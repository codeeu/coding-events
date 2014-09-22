#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeweekeu.settings")

	if sys.argv.index('test') == 1:
		import pytest
		sys.argv.pop(1)
		sys.exit(pytest.main())
	else:
		from django.core.management import execute_from_command_line
		execute_from_command_line(sys.argv)
