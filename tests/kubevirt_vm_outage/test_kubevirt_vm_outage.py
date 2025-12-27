import unittest
import time
from unittest.mock import MagicMock, patch

import yaml
from kubernetes.client.rest import ApiException
from krkn_lib.k8s import KrknKubernetes
from krkn_lib.models.telemetry import ScenarioTelemetry
from krkn_lib.telemetry.ocp import KrknTelemetryOpenshift
from krkn_lib.models.k8s import AffectedPod, PodsStatus

from krkn.scenario_plugins.kubevirt_vm_outage.kubevirt_vm_outage_scenario_plugin import KubevirtVmOutageScenarioPlugin


class TestKubevirtVmOutageScenarioPlugin(unittest.TestCase):
    
    def setUp(self):
        """
        Set up test fixtures for KubevirtVmOutageScenarioPlugin
        """
        self.plugin = KubevirtVmOutageScenarioPlugin()
        
        # Create mock k8s client
        self.k8s_client = MagicMock()
        self.custom_object_client = MagicMock()
        self.k8s_client.custom_object_client = self.custom_object_client
        self.plugin.k8s_client = self.k8s_client
        
        # Mock methods needed for KubeVirt operations
        self.k8s_client.list_custom_resource_definition = MagicMock()
        
        # Mock custom resource definition list with KubeVirt CRDs
        crd_list = MagicMock()
        crd_item = MagicMock()
        crd_item.spec = MagicMock()
        crd_item.spec.group = "kubevirt.io"
        crd_list.items = [crd_item]
        self.k8s_client.list_custom_resource_definition.return_value = crd_list
        
        # Mock VMI data
        self.mock_vmi = {
            "metadata": {
                "name": "test-vm",
                "namespace": "default"
            },
            "status": {
                "phase": "Running"
            }
        }
        
        # Create test config
        self.config = {
            "scenarios": [
                {
                    "name": "kubevirt outage test",
                    "scenario": "kubevirt_vm_outage",
                    "parameters": {
                        "vm_name": "test-vm",
                        "namespace": "default",
                        "duration": 0  
                    }
                }
            ]
        }
        
        # Create a temporary config file
        import tempfile, os
        temp_dir = tempfile.gettempdir()
        self.scenario_file = os.path.join(temp_dir, "test_kubevirt_scenario.yaml")
        with open(self.scenario_file, "w") as f:
            yaml.dump(self.config, f)
            
        # Mock dependencies
        self.telemetry = MagicMock(spec=KrknTelemetryOpenshift)
        self.scenario_telemetry = MagicMock(spec=ScenarioTelemetry)
        self.telemetry.get_lib_kubernetes.return_value = self.k8s_client
        
    def test_successful_injection_and_recovery(self):
        """
        Test successful deletion and recovery of a VMI
        """
        # Mock get_vmi to return our mock VMI
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                # Mock delete_vmi and wait_for_running to simulate success
                with patch.object(self.plugin, 'delete_vmi', return_value=0) as mock_delete:
                    with patch.object(self.plugin, 'wait_for_running', return_value=0) as mock_wait:
                        self.plugin.vmis_list = [self.mock_vmi]
                        self.plugin.pods_status = PodsStatus()
                        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
                        self.plugin.affected_pod.pod_readiness_time = 5.0
                        self.plugin.affected_pod.pod_rescheduling_time = 2.0
                        
                        with patch("builtins.open", unittest.mock.mock_open(read_data=yaml.dump(self.config))):
                            result = self.plugin.run("test-uuid", self.scenario_file, {}, self.telemetry, self.scenario_telemetry)
                        
        self.assertEqual(result, 0)
        mock_delete.assert_called_once_with("test-vm", "default", False)
        mock_wait.assert_called_once()
        
    def test_injection_failure(self):
        """
        Test failure during VMI deletion
        """
        # Mock get_vmi to return our mock VMI
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                # Mock delete_vmi to simulate failure
                with patch.object(self.plugin, 'delete_vmi', return_value=1) as mock_delete:
                    with patch.object(self.plugin, 'wait_for_running', return_value=0) as mock_wait:
                        self.plugin.vmis_list = [self.mock_vmi]
                        self.plugin.pods_status = PodsStatus()
                        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
                        
                        with patch("builtins.open", unittest.mock.mock_open(read_data=yaml.dump(self.config))):
                            result = self.plugin.run("test-uuid", self.scenario_file, {}, self.telemetry, self.scenario_telemetry)
                        
        self.assertEqual(result, 1)
        mock_delete.assert_called_once_with("test-vm", "default", False)
        mock_wait.assert_not_called()
        
    def test_disable_auto_restart(self):
        """
        Test VM auto-restart can be disabled
        """
        # Configure test with disable_auto_restart=True
        self.config["scenarios"][0]["parameters"]["disable_auto_restart"] = True
        
        # Mock VM object for patching
        mock_vm = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "spec": {}
        }
        
        # Mock get_vmi to return our mock VMI
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                # Mock VM patch operation
                with patch.object(self.plugin, 'patch_vm_spec') as mock_patch_vm:
                    mock_patch_vm.return_value = True
                    # Mock delete_vmi and wait_for_running
                    with patch.object(self.plugin, 'delete_vmi', return_value=0) as mock_delete:
                        with patch.object(self.plugin, 'wait_for_running', return_value=0) as mock_wait:
                            self.plugin.vmis_list = [self.mock_vmi]
                            self.plugin.pods_status = PodsStatus()
                            self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
                            self.plugin.affected_pod.pod_readiness_time = 5.0
                            self.plugin.affected_pod.pod_rescheduling_time = 2.0
                            
                            with patch("builtins.open", unittest.mock.mock_open(read_data=yaml.dump(self.config))):
                                result = self.plugin.run("test-uuid", self.scenario_file, {}, self.telemetry, self.scenario_telemetry)
        
        self.assertEqual(result, 0)
        # Should call delete_vmi with disable_auto_restart=True
        mock_delete.assert_called_once_with("test-vm", "default", True)
        mock_wait.assert_called_once()
        
    def test_recovery_when_vmi_does_not_exist(self):
        """
        Test recovery logic when VMI does not exist after deletion
        """
        # Store the original VMI in the plugin for recovery
        self.plugin.original_vmi = self.mock_vmi.copy()
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        # Create a cleaned vmi_dict as the plugin would
        vmi_dict = self.mock_vmi.copy()
        
        # Set up running VMI data for after recovery
        running_vmi = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        
        # Mock the custom object API to return success
        self.custom_object_client.create_namespaced_custom_object = MagicMock(return_value=running_vmi)
        
        # Run recovery with mocked time.sleep
        with patch('time.sleep'), patch('time.time', side_effect=[0, 5, 10, 15]):
            with patch.object(self.plugin, 'get_vmi', side_effect=[None, None, running_vmi]):
                with patch.object(self.plugin, 'wait_for_running', return_value=0):
                    result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 0)
    
    def test_validation_failure(self):
        """
        Test validation failure when KubeVirt is not installed
        """
        # Mock empty CRD list (no KubeVirt CRDs)
        empty_crd_list = MagicMock()
        empty_crd_list.items = []
        
        self.plugin.vmis_list = []  # No VMIs to process
        
        with patch("builtins.open", unittest.mock.mock_open(read_data=yaml.dump(self.config))):
            result = self.plugin.run("test-uuid", self.scenario_file, {}, self.telemetry, self.scenario_telemetry)
            
        self.assertEqual(result, 0)
        
    def test_delete_vmi_timeout(self):
        """
        Test timeout during VMI deletion
        """
        # Mock successful delete operation
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(return_value={})
        self.plugin.original_vmi = self.mock_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        # Mock that get_vmi always returns VMI (never gets deleted)
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            # Use a counter to provide time.time values
            time_counter = [0]
            def mock_time_func():
                time_counter[0] += 10
                return time_counter[0]
            
            with patch('time.sleep'), patch('time.time', side_effect=mock_time_func):
                result = self.plugin.delete_vmi("test-vm", "default", False)
            
        self.assertEqual(result, 1)
        self.custom_object_client.delete_namespaced_custom_object.assert_called_once_with(
            group="kubevirt.io",
            version="v1",
            namespace="default",
            plural="virtualmachineinstances",
            name="test-vm"
        )


    def test_get_vmi_api_error(self):
        """
        Test API error handling in get_vmi
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        self.custom_object_client.get_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        with self.assertRaises(ApiException):
            self.plugin.get_vmi("test-vm", "default")
    
    def test_get_vmi_unexpected_error(self):
        """
        Test unexpected error handling in get_vmi
        """
        self.custom_object_client.get_namespaced_custom_object = MagicMock(side_effect=Exception("Unexpected error"))
        
        with self.assertRaises(Exception):
            self.plugin.get_vmi("test-vm", "default")
    
    def test_get_vmis_with_regex_pattern(self):
        """
        Test get_vmis with regex pattern matching
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        vmis_response = {
            "items": [
                {
                    "metadata": {"name": "test-vm-1", "namespace": "default"},
                    "status": {"phase": "Running"}
                },
                {
                    "metadata": {"name": "test-vm-2", "namespace": "default"},
                    "status": {"phase": "Running"}
                },
                {
                    "metadata": {"name": "other-vm", "namespace": "default"},
                    "status": {"phase": "Running"}
                }
            ]
        }
        
        self.k8s_client.list_namespaces_by_regex = MagicMock(return_value=["default"])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(return_value=vmis_response)
        
        self.plugin.get_vmis("test-vm-.*", "default")
        
        # Should only match test-vm-1 and test-vm-2
        self.assertEqual(len(self.plugin.vmis_list), 2)
    
    def test_get_vmis_api_error(self):
        """
        Test API error handling in get_vmis
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        self.k8s_client.list_namespaces_by_regex = MagicMock(return_value=["default"])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        with self.assertRaises(ApiException):
            self.plugin.get_vmis("test-vm", "default")
    
    def test_get_vmis_unexpected_error(self):
        """
        Test unexpected error handling in get_vmis
        """
        self.k8s_client.list_namespaces_by_regex = MagicMock(return_value=["default"])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(side_effect=Exception("Unexpected error"))
        
        with self.assertRaises(Exception):
            self.plugin.get_vmis("test-vm", "default")
    
    def test_patch_vm_spec_failure(self):
        """
        Test patch_vm_spec when patch operation fails
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        
        mock_vm = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "spec": {}
        }
        
        self.custom_object_client.get_namespaced_custom_object = MagicMock(return_value=mock_vm)
        self.custom_object_client.patch_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        result = self.plugin.patch_vm_spec("test-vm", "default", True)
        self.assertFalse(result)
    
    def test_patch_vm_spec_unexpected_error(self):
        """
        Test patch_vm_spec with unexpected error
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.get_namespaced_custom_object = MagicMock(side_effect=Exception("Unexpected error"))
        
        result = self.plugin.patch_vm_spec("test-vm", "default", True)
        self.assertFalse(result)
    
    def test_delete_vmi_404_error(self):
        """
        Test delete_vmi when VMI returns 404 error
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=404)
        api_exception.status = 404
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        self.plugin.original_vmi = self.mock_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        result = self.plugin.delete_vmi("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_delete_vmi_api_error(self):
        """
        Test delete_vmi with API error
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        self.plugin.original_vmi = self.mock_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        result = self.plugin.delete_vmi("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_delete_vmi_exception(self):
        """
        Test delete_vmi with unexpected exception
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(side_effect=Exception("Unexpected error"))
        
        self.plugin.original_vmi = self.mock_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        result = self.plugin.delete_vmi("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_delete_vmi_with_auto_restart_disabled(self):
        """
        Test delete_vmi with auto-restart disabled
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(return_value={})
        self.plugin.original_vmi = self.mock_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        with patch.object(self.plugin, 'get_vmi', return_value=None):
            with patch.object(self.plugin, 'patch_vm_spec', return_value=True) as mock_patch:
                # Use a counter to provide time.time values
                time_counter = [0]
                def mock_time_func():
                    time_counter[0] += 10
                    return time_counter[0]
                
                with patch('time.sleep'), patch('time.time', side_effect=mock_time_func):
                    result = self.plugin.delete_vmi("test-vm", "default", disable_auto_restart=True)
        
        mock_patch.assert_called_once_with("test-vm", "default", running=False)
        self.assertEqual(result, 1)
    
    def test_validate_environment_api_error(self):
        """
        Test validate_environment with API error
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        self.custom_object_client.list_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        result = self.plugin.validate_environment("test-vm", "default")
        self.assertFalse(result)
    
    def test_validate_environment_vmi_not_found(self):
        """
        Test validate_environment when VMI doesn't exist
        """
        crd_list = MagicMock()
        crd_item = MagicMock()
        crd_list.items = [crd_item]
        self.custom_object_client.list_namespaced_custom_object = MagicMock(return_value=crd_list)
        
        with patch.object(self.plugin, 'get_vmi', return_value=None):
            result = self.plugin.validate_environment("test-vm", "default")
        
        self.assertFalse(result)
    
    def test_wait_for_running_timeout(self):
        """
        Test wait_for_running timeout scenario
        """
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        with patch('time.sleep'), patch('time.time', side_effect=[0, 10, 20, 130, 130]):
            with patch.object(self.plugin, 'get_vmi', return_value=None):
                result = self.plugin.wait_for_running("test-vm", "default", timeout=120)
        
        self.assertEqual(result, 1)
    
    def test_wait_for_running_vmi_not_running(self):
        """
        Test wait_for_running when VMI exists but not in Running state
        """
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        not_running_vmi = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "status": {"phase": "Pending"}
        }
        
        running_vmi = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        
        with patch('time.sleep'), patch('time.time', side_effect=[0, 5, 10, 15, 20, 25]):
            with patch.object(self.plugin, 'get_vmi', side_effect=[not_running_vmi, not_running_vmi, running_vmi]):
                result = self.plugin.wait_for_running("test-vm", "default", timeout=30)
        
        self.assertEqual(result, 0)
    
    def test_execute_scenario_missing_vm_name(self):
        """
        Test execute_scenario with missing vm_name parameter
        """
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "namespace": "default"
            }
        }
        
        result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(result, 1)
    
    def test_execute_scenario_vmi_not_found_after_get_vmis(self):
        """
        Test execute_scenario when VMI is not found after get_vmis
        """
        self.plugin.vmis_list = []
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'get_vmis', return_value=None):
            result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        # Should handle gracefully, but with empty list will skip loop
        self.assertEqual(result, self.plugin.pods_status)
    
    def test_execute_scenario_validation_failure(self):
        """
        Test execute_scenario when validation fails
        """
        self.plugin.vmis_list = [self.mock_vmi]
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'validate_environment', return_value=False):
            result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(result, 1)
    
    def test_execute_scenario_delete_vmi_failure(self):
        """
        Test execute_scenario when delete_vmi fails
        """
        self.plugin.vmis_list = [self.mock_vmi]
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                with patch.object(self.plugin, 'delete_vmi', return_value=1):
                    result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(result.unrecovered[0].pod_name, "test-vm")
    
    def test_execute_scenario_wait_for_running_failure(self):
        """
        Test execute_scenario when wait_for_running fails
        """
        self.plugin.vmis_list = [self.mock_vmi]
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                with patch.object(self.plugin, 'delete_vmi', return_value=0):
                    with patch.object(self.plugin, 'wait_for_running', return_value=1):
                        result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(result.unrecovered[0].pod_name, "test-vm")
    
    def test_execute_scenario_multiple_kill_count(self):
        """
        Test execute_scenario with multiple kill_count
        """
        mock_vmi_1 = {
            "metadata": {"name": "test-vm-1", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        mock_vmi_2 = {
            "metadata": {"name": "test-vm-2", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        
        self.plugin.vmis_list = [mock_vmi_1, mock_vmi_2]
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm-.*",
                "namespace": "default",
                "kill_count": 2
            }
        }
        
        def setup_affected_pod(*args, **kwargs):
            self.plugin.affected_pod.pod_readiness_time = 5.0
            self.plugin.affected_pod.pod_rescheduling_time = 2.0
            return 0
        
        with patch.object(self.plugin, 'get_vmi', side_effect=[mock_vmi_1, mock_vmi_2]):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                with patch.object(self.plugin, 'delete_vmi', return_value=0):
                    with patch.object(self.plugin, 'wait_for_running', side_effect=setup_affected_pod):
                        result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(len(result.recovered), 2)
    
    def test_execute_scenario_exception(self):
        """
        Test execute_scenario exception handling
        """
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'get_vmis', side_effect=Exception("Test error")):
            result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        self.assertEqual(result, self.plugin.pods_status)
    
    def test_run_file_not_found(self):
        """
        Test run method when scenario file is not found
        """
        result = self.plugin.run("test-uuid", "/nonexistent/file.yaml", {}, self.telemetry, self.scenario_telemetry)
        
        self.assertEqual(result, 1)
    
    def test_run_invalid_yaml(self):
        """
        Test run method with invalid YAML
        """
        import tempfile, os
        temp_dir = tempfile.gettempdir()
        scenario_file = os.path.join(temp_dir, "test_invalid_yaml.yaml")
        with open(scenario_file, "w") as f:
            f.write("invalid: yaml: content:")
        
        try:
            result = self.plugin.run("test-uuid", scenario_file, {}, self.telemetry, self.scenario_telemetry)
        finally:
            if os.path.exists(scenario_file):
                os.remove(scenario_file)
    
    def test_run_no_matching_scenario(self):
        """
        Test run method when no matching scenario is found
        """
        config = {
            "scenarios": [
                {
                    "name": "other scenario",
                    "scenario": "other_scenario",
                    "parameters": {}
                }
            ]
        }
        
        import tempfile, os
        temp_dir = tempfile.gettempdir()
        scenario_file = os.path.join(temp_dir, "test_other_scenario.yaml")
        with open(scenario_file, "w") as f:
            yaml.dump(config, f)
        
        try:
            result = self.plugin.run("test-uuid", scenario_file, {}, self.telemetry, self.scenario_telemetry)
            self.assertEqual(result, 0)
        finally:
            if os.path.exists(scenario_file):
                os.remove(scenario_file)
    
    def test_run_with_unrecovered_pods(self):
        """
        Test run method returns 1 when there are unrecovered pods
        """
        config = {
            "scenarios": [
                {
                    "name": "kubevirt outage test",
                    "scenario": "kubevirt_vm_outage",
                    "parameters": {
                        "vm_name": "test-vm",
                        "namespace": "default"
                    }
                }
            ]
        }
        
        import tempfile, os
        temp_dir = tempfile.gettempdir()
        scenario_file = os.path.join(temp_dir, "test_unrecovered.yaml")
        with open(scenario_file, "w") as f:
            yaml.dump(config, f)
        
        try:
            self.plugin.vmis_list = [self.mock_vmi]
            with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
                with patch.object(self.plugin, 'validate_environment', return_value=True):
                    with patch.object(self.plugin, 'delete_vmi', return_value=1):
                        result = self.plugin.run("test-uuid", scenario_file, {}, self.telemetry, self.scenario_telemetry)
            
            self.assertEqual(result, 1)
        finally:
            if os.path.exists(scenario_file):
                os.remove(scenario_file)
    
    def test_recover_no_original_vmi(self):
        """
        Test recover when no original VMI was captured
        """
        self.plugin.original_vmi = None
        
        result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_recover_with_create_error(self):
        """
        Test recover when create operation fails
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=500)
        api_exception.status = 500
        self.custom_object_client.create_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        self.plugin.original_vmi = self.mock_vmi
        
        result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_recover_with_unexpected_error_during_create(self):
        """
        Test recover with unexpected error during create
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.create_namespaced_custom_object = MagicMock(side_effect=Exception("Unexpected error"))
        
        self.plugin.original_vmi = self.mock_vmi
        
        result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 1)
    
    def test_get_scenario_types(self):
        """
        Test get_scenario_types returns correct types
        """
        types = self.plugin.get_scenario_types()
        
        self.assertEqual(types, ["kubevirt_vm_outage"])
    
    def test_init_clients(self):
        """
        Test init_clients initializes client properly
        """
        k8s_client = MagicMock()
        custom_object_client = MagicMock()
        k8s_client.custom_object_client = custom_object_client
        
        self.plugin.init_clients(k8s_client)
        
        self.assertEqual(self.plugin.k8s_client, k8s_client)
        self.assertEqual(self.plugin.custom_object_client, custom_object_client)

    def test_get_vmi_404_not_found(self):
        """
        Test get_vmi when VMI returns 404 (not found)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=404)
        api_exception.status = 404
        self.custom_object_client.get_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        result = self.plugin.get_vmi("test-vm", "default")
        
        self.assertIsNone(result)

    def test_get_vmis_404_not_found(self):
        """
        Test get_vmis when returns 404 (not found)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        api_exception = ApiException(status=404)
        api_exception.status = 404
        self.k8s_client.list_namespaces_by_regex = MagicMock(return_value=["default"])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(side_effect=api_exception)
        
        # Should not raise, just log warning
        self.plugin.get_vmis("test-vm", "default")

    def test_execute_scenario_with_empty_vmis_list(self):
        """
        Test execute_scenario when vmis_list is empty after get_vmis
        """
        self.plugin.vmis_list = []
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        # Should return pods_status (empty)
        self.assertEqual(len(result.recovered), 0)
        self.assertEqual(len(result.unrecovered), 0)

    def test_validate_environment_exception(self):
        """
        Test validate_environment with exception
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.list_namespaced_custom_object = MagicMock(side_effect=Exception("Test error"))
        
        result = self.plugin.validate_environment("test-vm", "default")
        
        self.assertFalse(result)

    def test_patch_vm_spec_success(self):
        """
        Test patch_vm_spec successful patching
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        mock_vm = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "spec": {}
        }
        
        self.custom_object_client.get_namespaced_custom_object = MagicMock(return_value=mock_vm)
        self.custom_object_client.patch_namespaced_custom_object = MagicMock(return_value=mock_vm)
        
        result = self.plugin.patch_vm_spec("test-vm", "default", True)
        
        self.assertTrue(result)
        self.custom_object_client.patch_namespaced_custom_object.assert_called_once()

    def test_delete_vmi_successfully_deleted(self):
        """
        Test delete_vmi when VMI is successfully recreated with new timestamp
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(return_value={})
        
        # Original VMI with old timestamp
        original_vmi = self.mock_vmi.copy()
        original_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        original_vmi['metadata']['creationTimestamp'] = '2025-01-01T00:00:00Z'
        self.plugin.original_vmi = original_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        # Recreated VMI with new timestamp
        recreated_vmi = self.mock_vmi.copy()
        recreated_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        recreated_vmi['metadata']['creationTimestamp'] = '2025-01-02T00:00:00Z'
        
        with patch.object(self.plugin, 'get_vmi', return_value=recreated_vmi):
            with patch('time.sleep'), patch('time.time', return_value=10):
                result = self.plugin.delete_vmi("test-vm", "default", False)
        
        self.assertEqual(result, 0)

    def test_wait_for_running_immediately_running(self):
        """
        Test wait_for_running when VMI is already running
        """
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        running_vmi = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        
        with patch('time.sleep'), patch('time.time', side_effect=[0, 1, 2]):
            with patch.object(self.plugin, 'get_vmi', return_value=running_vmi):
                result = self.plugin.wait_for_running("test-vm", "default", timeout=120)
        
        self.assertEqual(result, 0)

    def test_recover_exception_outer(self):
        """
        Test recover with exception in outer try block
        """
        self.plugin.original_vmi = self.mock_vmi
        
        # Make get_vmi throw exception to trigger outer exception handling
        with patch.object(self.plugin, 'wait_for_running', side_effect=Exception("Test error")):
            self.plugin.k8s_client = self.k8s_client
            self.plugin.custom_object_client = self.custom_object_client
            self.custom_object_client.create_namespaced_custom_object = MagicMock(return_value=self.mock_vmi)
            
            result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 1)

    def test_execute_scenario_get_vmi_returns_none(self):
        """
        Test execute_scenario when get_vmi returns None
        """
        self.plugin.vmis_list = [self.mock_vmi]
        
        config = {
            "scenario": "kubevirt_vm_outage",
            "parameters": {
                "vm_name": "test-vm",
                "namespace": "default"
            }
        }
        
        with patch.object(self.plugin, 'get_vmi', return_value=None):
            with patch.object(self.plugin, 'validate_environment', return_value=True):
                result = self.plugin.execute_scenario(config, self.scenario_telemetry)
        
        # Should return 1 when VMI not found
        self.assertEqual(result, 1)

    def test_delete_vmi_vmi_recreated(self):
        """
        Test delete_vmi when VMI is recreated (creation timestamp changes)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(return_value={})
        
        # Original VMI with old timestamp
        original_vmi = self.mock_vmi.copy()
        original_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        original_vmi['metadata']['creationTimestamp'] = '2025-01-01T00:00:00Z'
        self.plugin.original_vmi = original_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        # Recreated VMI with different creation timestamp
        recreated_vmi = self.mock_vmi.copy()
        recreated_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        recreated_vmi['metadata']['creationTimestamp'] = '2025-01-02T00:00:00Z'
        
        with patch.object(self.plugin, 'get_vmi', return_value=recreated_vmi):
            with patch('time.sleep'), patch('time.time', return_value=10):
                result = self.plugin.delete_vmi("test-vm", "default", False)
        
        self.assertEqual(result, 0)

    def test_run_with_merge_multiple_scenarios(self):
        """
        Test run method merges results from multiple scenarios
        """
        config = {
            "scenarios": [
                {
                    "name": "scenario 1",
                    "scenario": "kubevirt_vm_outage",
                    "parameters": {
                        "vm_name": "test-vm",
                        "namespace": "default"
                    }
                },
                {
                    "name": "scenario 2",
                    "scenario": "kubevirt_vm_outage",
                    "parameters": {
                        "vm_name": "test-vm",
                        "namespace": "default"
                    }
                }
            ]
        }
        
        import tempfile, os
        temp_dir = tempfile.gettempdir()
        scenario_file = os.path.join(temp_dir, "test_multi_scenario.yaml")
        with open(scenario_file, "w") as f:
            yaml.dump(config, f)
        
        try:
            self.plugin.vmis_list = [self.mock_vmi, self.mock_vmi]
            
            def mock_wait_for_running(*args, **kwargs):
                self.plugin.affected_pod.pod_readiness_time = 5.0
                self.plugin.affected_pod.pod_rescheduling_time = 2.0
                return 0
            
            with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
                with patch.object(self.plugin, 'validate_environment', return_value=True):
                    with patch.object(self.plugin, 'delete_vmi', return_value=0):
                        with patch.object(self.plugin, 'wait_for_running', side_effect=mock_wait_for_running):
                            result = self.plugin.run("test-uuid", scenario_file, {}, self.telemetry, self.scenario_telemetry)
        finally:
            if os.path.exists(scenario_file):
                os.remove(scenario_file)

    def test_validate_environment_success(self):
        """
        Test validate_environment success path
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        crd_list = MagicMock()
        crd_list.items = MagicMock(return_value=[MagicMock()])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(return_value=crd_list)
        
        with patch.object(self.plugin, 'get_vmi', return_value=self.mock_vmi):
            result = self.plugin.validate_environment("test-vm", "default")
        
        self.assertTrue(result)

    def test_get_vmi_success(self):
        """
        Test get_vmi returns VMI successfully (covers line 90)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.get_namespaced_custom_object = MagicMock(return_value=self.mock_vmi)
        
        result = self.plugin.get_vmi("test-vm", "default")
        
        self.assertEqual(result, self.mock_vmi)
        self.custom_object_client.get_namespaced_custom_object.assert_called_once_with(
            group="kubevirt.io",
            version="v1",
            namespace="default",
            plural="virtualmachineinstances",
            name="test-vm"
        )

    def test_validate_environment_empty_crd_list(self):
        """
        Test validate_environment when CRD list is empty (covers lines 219-220)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        crd_list = MagicMock()
        crd_list.items = MagicMock(return_value=[])  # Empty CRD list
        self.custom_object_client.list_namespaced_custom_object = MagicMock(return_value=crd_list)
        
        result = self.plugin.validate_environment("test-vm", "default")
        
        self.assertFalse(result)

    def test_validate_environment_vmi_not_found_after_crd_check(self):
        """
        Test validate_environment when VMI not found after CRD check (covers lines 225-226)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        crd_list = MagicMock()
        crd_list.items = MagicMock(return_value=[MagicMock()])
        self.custom_object_client.list_namespaced_custom_object = MagicMock(return_value=crd_list)
        
        with patch.object(self.plugin, 'get_vmi', return_value=None):
            result = self.plugin.validate_environment("test-vm", "default")
        
        self.assertFalse(result)

    def test_patch_vm_spec_no_spec_field(self):
        """
        Test patch_vm_spec when VM has no spec field (covers line 256)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        # VM without spec field
        mock_vm = {
            "metadata": {"name": "test-vm", "namespace": "default"}
            # No "spec" field
        }
        
        self.custom_object_client.get_namespaced_custom_object = MagicMock(return_value=mock_vm)
        self.custom_object_client.patch_namespaced_custom_object = MagicMock(return_value=mock_vm)
        
        result = self.plugin.patch_vm_spec("test-vm", "default", True)
        
        self.assertTrue(result)
        # Verify spec was added
        call_args = self.custom_object_client.patch_namespaced_custom_object.call_args
        self.assertIn('spec', call_args[1]['body'])
        self.assertEqual(call_args[1]['body']['spec']['running'], True)

    def test_delete_vmi_with_failed_patch(self):
        """
        Test delete_vmi when patch_vm_spec fails but continues (covers line 292)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        self.custom_object_client.delete_namespaced_custom_object = MagicMock(return_value={})
        
        # Original VMI with old timestamp
        original_vmi = self.mock_vmi.copy()
        original_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        original_vmi['metadata']['creationTimestamp'] = '2025-01-01T00:00:00Z'
        self.plugin.original_vmi = original_vmi
        self.plugin.pods_status = PodsStatus()
        self.plugin.affected_pod = AffectedPod(pod_name="test-vm", namespace="default")
        
        # Recreated VMI with new timestamp
        recreated_vmi = self.mock_vmi.copy()
        recreated_vmi['metadata'] = self.mock_vmi['metadata'].copy()
        recreated_vmi['metadata']['creationTimestamp'] = '2025-01-02T00:00:00Z'
        
        # patch_vm_spec returns False (failed), but deletion continues
        with patch.object(self.plugin, 'patch_vm_spec', return_value=False):
            with patch.object(self.plugin, 'get_vmi', return_value=recreated_vmi):
                with patch('time.sleep'), patch('time.time', return_value=10):
                    result = self.plugin.delete_vmi("test-vm", "default", True)  # disable_auto_restart=True
        
        self.assertEqual(result, 0)

    def test_recover_with_metadata_fields(self):
        """
        Test recover cleans up metadata fields correctly (covers line 378)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        # VMI with all metadata fields that need cleanup
        original_vmi = {
            "metadata": {
                "name": "test-vm",
                "namespace": "default",
                "resourceVersion": "12345",
                "uid": "abc-123",
                "creationTimestamp": "2025-01-01T00:00:00Z",
                "generation": 1
            },
            "status": {"phase": "Running"}
        }
        self.plugin.original_vmi = original_vmi
        
        running_vmi = {
            "metadata": {"name": "test-vm", "namespace": "default"},
            "status": {"phase": "Running"}
        }
        self.custom_object_client.create_namespaced_custom_object = MagicMock(return_value=running_vmi)
        
        with patch.object(self.plugin, 'wait_for_running', return_value=0):
            result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 0)
        # Verify create was called with cleaned metadata
        call_args = self.custom_object_client.create_namespaced_custom_object.call_args
        body = call_args[1]['body']
        self.assertNotIn('resourceVersion', body['metadata'])
        self.assertNotIn('uid', body['metadata'])
        self.assertNotIn('creationTimestamp', body['metadata'])
        self.assertNotIn('generation', body['metadata'])

    def test_recover_outer_exception(self):
        """
        Test recover handles outer exception (covers lines 404-407)
        """
        self.plugin.k8s_client = self.k8s_client
        self.plugin.custom_object_client = self.custom_object_client
        
        # Set original_vmi to None to trigger exception path
        self.plugin.original_vmi = None
        
        # This will hit the else branch and return 1
        result = self.plugin.recover("test-vm", "default", False)
        
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
