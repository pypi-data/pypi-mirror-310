import os
import shutil
import time
import unittest

from click.testing import CliRunner

from unfurl.job import JobOptions, Runner
from unfurl.localenv import LocalEnv
from unfurl.support import Status
from unfurl.util import sensitive_str

from .utils import lifecycle, MotoTest


@unittest.skipIf(
    "terraform" in os.getenv("UNFURL_TEST_SKIP", ""), "UNFURL_TEST_SKIP set"
)
class TerraformTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def setup_filesystem(self):
        terraform_dir = os.environ["terraform_dir"] = os.path.join(
            os.path.dirname(__file__), "fixtures", "terraform"
        )

        path = os.path.join(os.path.dirname(__file__), "examples")
        shutil.copy(
            os.path.join(path, "terraform-simple-ensemble.yaml"), "ensemble.yaml"
        )

        # copy the terraform lock file so the configurator avoids calling terraform init
        # if .tox/.terraform already has the providers
        os.makedirs("tasks/terraform-node")
        lock_file = terraform_dir + "/.terraform.lock.hcl"
        if not os.getenv("CI") and os.path.exists(lock_file):
            shutil.copy(lock_file, "tasks/terraform-node/")
            os.makedirs("tasks/terraform-node-json")
            shutil.copy(lock_file, "tasks/terraform-node-json/")

    def test_terraform(self):
        cli_runner = CliRunner()
        with cli_runner.isolated_filesystem():
            self.setup_filesystem()
            manifest = LocalEnv().get_manifest()
            runner = Runner(manifest)
            job = runner.run(JobOptions(startTime=1, check=True))  # deploy
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            example = job.rootResource.find_resource("example")
            self.assertEqual(example.attributes["tag"], "Hello, test!")
            rtt = job.rootResource.find_resource("result-template-test")
            self.assertEqual(rtt.attributes["test"], "outputting result template test!")

            summary = job.json_summary()
            task_outputs = set(
                [
                    tuple(task.result.outputs.values())[0]
                    for task in job.workDone.values()
                    if task.result.outputs
                ]
            )
            assert task_outputs == {
                "outputting result template test!",
                "outputting test3!",
                "outputting test2!",
                "Hello, test!",
            }
            terraform_node = job.rootResource.find_resource("terraform-node")
            self.assertEqual(
                terraform_node.attributes["test_output"], "outputting test2!"
            )

            # print(job.summary())
            # print(job._planSummary())
            # print(json.dumps(summary, indent=2))
            self.assertEqual(
                {
                    "job": {
                        "id": "A01110000000",
                        "status": "ok",
                        "total": 8,
                        "ok": 8,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 8,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "result-template-test",
                            "operation": "check",
                            "template": "result-template-test",
                            "type": "TerraformWithResultTemplate",
                            "targetStatus": "absent",
                            "targetState": "initial",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "result-template-test",
                            "operation": "configure",
                            "template": "result-template-test",
                            "type": "TerraformWithResultTemplate",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "add",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node",
                            "operation": "check",
                            "template": "terraform-node",
                            "type": "GenericTerraformManagedResource",
                            "targetStatus": "absent",
                            "targetState": "initial",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node",
                            "operation": "configure",
                            "template": "terraform-node",
                            "type": "GenericTerraformManagedResource",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "add",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node-json",
                            "operation": "check",
                            "template": "terraform-node-json",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "initial",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node-json",
                            "operation": "configure",
                            "template": "terraform-node-json",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "add",
                        },
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "check",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",  # nothing to modify... but still needs to run!
                            "targetState": "initial",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "configure",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "add",
                        },
                    ],
                },
                summary,
            )

            runner2 = Runner(LocalEnv().get_manifest())
            job = runner2.run(JobOptions(workflow="undeploy", startTime=2))
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            # print(job.summary())
            summary = job.json_summary()
            # print(json.dumps(summary, indent=2))
            self.assertEqual(
                {
                    "job": {
                        "id": "A01120000000",
                        "status": "ok",
                        "total": 4,
                        "ok": 4,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 4,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "result-template-test",
                            "operation": "delete",
                            "template": "result-template-test",
                            "type": "TerraformWithResultTemplate",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "undeploy",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node",
                            "operation": "delete",
                            "template": "terraform-node",
                            "type": "GenericTerraformManagedResource",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "undeploy",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node-json",
                            "operation": "delete",
                            "template": "terraform-node-json",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "undeploy",
                        },
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "delete",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "undeploy",
                        },
                    ],
                },
                summary,
            )

            runner2 = Runner(LocalEnv().get_manifest())
            job = runner2.run(JobOptions(workflow="check", startTime=2))
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            summary = job.json_summary()
            # print(json.dumps(summary, indent=2))
            # print(job._json_plan_summary(True))
            self.assertEqual(
                {
                    "job": {
                        "id": "A01120GC0000",
                        "status": "ok",
                        "total": 4,
                        "ok": 4,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 0,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "result-template-test",
                            "operation": "check",
                            "template": "result-template-test",
                            "type": "TerraformWithResultTemplate",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": False,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node",
                            "operation": "check",
                            "template": "terraform-node",
                            "type": "GenericTerraformManagedResource",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": False,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "terraform-node-json",
                            "operation": "check",
                            "template": "terraform-node-json",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": False,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "check",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": False,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                    ],
                },
                summary,
            )
            self.assertEqual(
                job._json_plan_summary(include_rendered=False),
                [
                    {
                        "instance": "result-template-test",
                        "managed": "A01110000002",
                        "plan": [{"operation": "check", "reason": "check"}],
                        "state": "NodeState.deleted",
                        "status": "Status.absent",
                    },
                    {
                        "instance": "terraform-node",
                        "status": "Status.absent",
                        "state": "NodeState.deleted",
                        "managed": "A01110000004",
                        "plan": [{"operation": "check", "reason": "check"}],
                    },
                    {
                        "instance": "terraform-node-json",
                        "status": "Status.absent",
                        "state": "NodeState.deleted",
                        "managed": "A01110000006",
                        "plan": [{"operation": "check", "reason": "check"}],
                    },
                    {
                        "instance": "example",
                        "status": "Status.absent",
                        "state": "NodeState.deleted",
                        "managed": "A01110000008",
                        "plan": [{"operation": "check", "reason": "check"}],
                    },
                ],
            )

    @unittest.skipIf(
        "slow" in os.getenv("UNFURL_TEST_SKIP", ""), "UNFURL_TEST_SKIP set"
    )
    def test_lifecycle(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.setup_filesystem()
            for job in lifecycle(manifest=LocalEnv().get_manifest()):
                assert job.status == Status.ok


@unittest.skipIf(
    "terraform" in os.getenv("UNFURL_TEST_SKIP", ""), "UNFURL_TEST_SKIP set"
)
@unittest.skipIf("slow" in os.getenv("UNFURL_TEST_SKIP", ""), "UNFURL_TEST_SKIP set")
class TerraformMotoTest(MotoTest):
    def setUp(self):
        assert super().setUp(), "moto server didn't start"

        path = os.path.join(os.path.dirname(__file__), "examples")
        with open(os.path.join(path, "terraform-ensemble.yaml")) as f:
            self.ensemble_config = f.read()
        with open(os.path.join(path, "terraform-project-config.yaml")) as f:
            self.project_config = f.read()
        self.maxDiff = None

    def setup_filesystem(self):
        terraform_dir = os.environ["terraform_dir"] = os.path.join(
            os.path.dirname(__file__), "fixtures", "terraform"
        )

        # copy the terraform lock file so the configurator avoids calling terraform init
        # if .tox/.terraform already has the providers
        lock_file = terraform_dir + "/aws-terraform.lock.hcl"
        if not os.getenv("CI") and os.path.exists(lock_file):
            os.makedirs("tasks/example")
            shutil.copy(
                terraform_dir + "/aws-terraform.lock.hcl",
                "tasks/example/.terraform.lock.hcl",
            )

    def test_terraform(self):
        """
        test that runner figures out the proper tasks to run
        """
        runner = CliRunner()
        with runner.isolated_filesystem():
            self.setup_filesystem()
            with open("unfurl.yaml", "w") as f:
                f.write(self.project_config)

            with open("ensemble.yaml", "w") as f:
                f.write(self.ensemble_config)

            manifest = LocalEnv().get_manifest()
            assert manifest.manifest.vault and manifest.manifest.vault.secrets
            assert not manifest.lastJob

            job = Runner(manifest).run(JobOptions(startTime=1, check=True, verbose=-1))
            # print(job.out.getvalue())
            # print(job.jsonSummary(True))
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            assert job.status == Status.ok, job.summary()
            example = job.rootResource.find_resource("example")
            self.assertEqual(example.attributes["availability_zone"], "us-east-1a")
            self.assertEqual(
                type(example.attributes["availability_zone"]), sensitive_str
            )
            self.assertEqual(example.attributes["tags"], {"Name": "test"})
            # print("deploy")
            # print(job.jsonSummary(True))
            self.assertEqual(
                job.json_summary(),
                {
                    "job": {
                        "id": "A01110000000",
                        "status": "ok",
                        "total": 2,
                        "ok": 2,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 2,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "example",
                            "targetState": "initial",
                            "operation": "check",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        },
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "configure",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "add",
                        },
                    ],
                },
            )

            # reload and check
            manifest2 = LocalEnv().get_manifest()
            assert manifest2.lastJob
            manifest2.rootResource.find_resource("example")
            self.assertEqual(
                type(example.attributes["availability_zone"]), sensitive_str
            )
            job = Runner(manifest2).run(
                JobOptions(workflow="check", verbose=-1, startTime=2)
            )
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            # print("check")
            # print(job.jsonSummary(True))
            self.assertEqual(
                job.json_summary(),
                {
                    "job": {
                        "id": "A01120000000",
                        "status": "ok",
                        "total": 1,
                        "ok": 1,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 0,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "check",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "ok",
                            "targetState": "configured",
                            "changed": False,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "check",
                        }
                    ],
                },
            )
            assert job.status == Status.ok, job.summary()

            # reload and undeploy:
            manifest3 = LocalEnv().get_manifest()
            assert manifest3.lastJob
            example = manifest3.rootResource.find_resource("example")
            assert example
            self.assertEqual(
                type(example.attributes["availability_zone"]), sensitive_str
            )
            job = Runner(manifest3).run(
                JobOptions(workflow="undeploy", verbose=2, startTime=3)
            )
            assert not job.unexpectedAbort, job.unexpectedAbort.get_stack_trace()
            assert job.status == Status.ok, job.summary()
            self.assertEqual(
                job.json_summary(),
                {
                    "job": {
                        "id": "A01130000000",
                        "status": "ok",
                        "total": 1,
                        "ok": 1,
                        "error": 0,
                        "unknown": 0,
                        "skipped": 0,
                        "changed": 1,
                    },
                    "outputs": {},
                    "tasks": [
                        {
                            "status": "ok",
                            "target": "example",
                            "operation": "delete",
                            "template": "example",
                            "type": "unfurl.nodes.Installer.Terraform",
                            "targetStatus": "absent",
                            "targetState": "deleted",
                            "changed": True,
                            "configurator": "unfurl.configurators.terraform.TerraformConfigurator",
                            "priority": "required",
                            "reason": "undeploy",
                        }
                    ],
                },
            )
