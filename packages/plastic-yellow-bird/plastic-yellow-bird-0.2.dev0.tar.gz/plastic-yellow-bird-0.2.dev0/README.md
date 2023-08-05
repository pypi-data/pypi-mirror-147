# Plastic Yellow Bird (aka "PyB"): a Test and Observability Driven Development Framework for AWS CDK

`plastic-yellow-bird` is a test framework that introduces a whole new approach to monitoring, observability, and infrastructure development. It lets you to accomplish one thing as simply as possible: use the same code you write to verify your infrastructure as your monitoring and
alerting stack in production.

By using `plastic-yellow-bird`, your team can:

* write end-to-end functional and infrastructure tests as easily as you write unit or integration tests
* create AWS Synthetics Canaries with as little boilerplate as possible
* develop a planned production monitoring scheme from the project's outset
* harvest the effort spent writing automated functional tests as zero-cost, thoughtful baseline production monitoring

```python
import plastic_yellow_bird as pyb
import requests

@pyb.canary
def test_api_endpoint_returns_200_with_get(cdk_app):
    response = requests.get(cdk_app.api_stack.api.url)
    assert response.status_code == 200
```

Imagine you create the above test file in a CDK project directory that
contains an Amazon API Gateway CDK app. By using `plastic-yellow-bird`, which
is based on `pytest`, simply running `pytest`, `plastic-yellow-bird` would
deploy your CDK app and launch the `test_api_endpoint_returns_200_with_get` code
as an [AWS Synthetics Canary]() in the same account, then wait for the Canary to
run and report a status.  `plastic-yellow-bird` would then report this test's `Pass`
or `Fail` state just like any other `pytest` test result, based on the status of
the Canary. In other words, if the Canary launched by `plastic-yellow-bird`
succeeded, your test would be reported as passing, and if the Canary failed, the
test would be reported as failing.

## Design Principles

* Most use cases should require nothing more than test code and a decorator to indicate a PyB test
    * "Make simple things simple, and complex things possible" - Alan Kay
* Code should be beautiful
* Developers are smart and capable of doing incredibly difficult things, but using this tool shouldn't be one of those incredibly difficult things
* If no one uses this in real projects, we've failed