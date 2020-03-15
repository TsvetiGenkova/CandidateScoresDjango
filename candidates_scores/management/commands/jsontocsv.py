from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for json_file in options['json_file']:
            try:
                tmp_data = pd.read_json(json_file, orient='records') 
                tmp_data["score"] = pd.to_numeric(tmp_data["score"], downcast='float')
                schema = pandas_schema.Schema([Column('candidate_ref', [MatchesPatternValidation(r'[A-Za-z0-9]{8}')]), 
                    Column('name', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]), 
                    Column('score', [InRangeValidation(0.0, 100.0)])])
                errors = schema.validate(tmp_data)
                errors_index_rows = [e.row for e in errors]
                data_clean = tmp_data.drop(index=errors_index_rows)
                data_clean.sort_values(by=["score"], ascending=False, inplace=True)
                data_clean.to_csv('canidates_from_json.csv', header=True, index=False) 

            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    json_file))

