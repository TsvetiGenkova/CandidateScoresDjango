from django.core.management.base import BaseCommand, CommandError
from candidates_scores.models import Candidate, Score
import pandas as pd
import re
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)


    def handle(self, *args, **options):
        for csv_file in options['csv_file']:
            try:
                tmp_data = pd.read_csv(csv_file, sep=',', skipinitialspace=True)
                tmp_data["score"] = pd.to_numeric(tmp_data["score"], downcast='float')
                schema = pandas_schema.Schema([Column('candidate_ref', [MatchesPatternValidation(r'[A-Za-z0-9]{8}')]), 
                    Column('name', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]), 
                    Column('score', [InRangeValidation(0.0, 100.0)])])
                errors = schema.validate(tmp_data)
                errors_index_rows = [e.row for e in errors]
                data_clean = tmp_data.drop(index=errors_index_rows)
                candidates = [Candidate(name = row['name'],
                                        candidate_ref = row['candidate_ref'],) 
                             for index, row in data_clean.drop(columns=['score']).drop_duplicates().iterrows()]

                Candidate.objects.bulk_create(candidates, ignore_conflicts=True)

                scores = [Score(score = row['score'], 
                                candidate = Candidate.objects.get(candidate_ref=row["candidate_ref"]))
                         for index, row in data_clean.iterrows()]
            
                Score.objects.bulk_create(scores, ignore_conflicts=True)

            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    csv_file))