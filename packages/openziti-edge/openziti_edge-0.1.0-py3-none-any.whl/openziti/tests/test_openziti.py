import pytest
import openziti


def test_project_defines_author_and_version():
    assert hasattr(openziti, '__author__')
    assert hasattr(openziti, '__version__')
