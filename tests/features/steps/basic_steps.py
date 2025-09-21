import importlib

from behave import then, when


@when('I try to import "{package_name}"')
def step_when_import(context, package_name):
    context.package_name = package_name
    try:
        context.pkg = importlib.import_module(package_name)
        context.import_failed = False
    except ImportError:
        context.import_failed = True


@then("it should be importable")
def step_then_check(context):
    assert not context.import_failed, (
        f"Пакет {context.package_name} " "не импортируется!"
    )
