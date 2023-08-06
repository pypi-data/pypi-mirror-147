from credmark.client import CredmarkClient
from credmark.client.errors import ModelBaseError


def main():
    client = CredmarkClient()
    try:
        result = client.run_model('example.echo', raise_error_results=True)
        print(result['output'])
    except ModelBaseError as err:
        print('Model Error:', str(err), err.data)
    except Exception as err:
        # requests/urllib exception
        print('Exception', str(err))


if __name__ == '__main__':
    main()
