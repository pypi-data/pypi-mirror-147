import sys


def main():
    try:
        from pdf2image_cli.core import main
        statusCode = main()

    except KeyboardInterrupt:
        from pdf2image_cli.status import ExitStatus
        statusCode = ExitStatus.ERROR_CTRL_C

    return statusCode.value


if __name__ == "__main__":
    sys.exit(main())
