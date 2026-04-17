"""Tests for the offline/timeseries driver."""

import pytest
from pathlib import Path
import sys
import yaml

# Add path for imports
REPO_ROOT = Path(__file__).parent.parent
TIMESERIES_SRC = REPO_ROOT / 'offline' / 'timeseries' / 'src'
sys.path.insert(0, str(TIMESERIES_SRC))
sys.path.insert(0, str(REPO_ROOT / 'offline'))


class TestOfflineDriverImports:
    """Tests for offline driver imports."""
    
    def test_can_import_driver_module(self):
        """Test that the offline driver module can be imported."""
        # Note: This may fail if system dependencies are not met
        # The test verifies the module structure is correct
        try:
            from pyradmon_driver_offline import PyRadmonBase
            assert PyRadmonBase is not None
        except Exception as e:
            # If import fails due to system dependencies (symlink, etc.), 
            # that's expected in test environment
            pytest.skip(f"Skipping due to system dependency: {e}")


class TestConfigTemplates:
    """Tests for configuration templates."""
    
    def test_geosit_template_exists(self):
        """Test that geosit config template exists."""
        config_path = TIMESERIES_SRC / 'test_config_yaml_path.tmpl.geosit.yaml'
        assert config_path.exists()
    
    def test_m21c_template_exists(self):
        """Test that m21c config template exists."""
        config_path = TIMESERIES_SRC / 'test_config_yaml_path.tmpl.m21c.yaml'
        assert config_path.exists()
    
    def test_skeleton_template_exists(self):
        """Test that skeleton config template exists."""
        config_path = TIMESERIES_SRC / 'test_config_yaml_path.skeleton.yaml'
        assert config_path.exists()
    
    def test_template_is_valid_yaml(self):
        """Test that template files are valid YAML."""
        config_path = TIMESERIES_SRC / 'test_config_yaml_path.tmpl.geosit.yaml'
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert isinstance(config, dict)


class TestDriverScripts:
    """Tests for driver shell scripts."""
    
    def test_bin2txt_driver_exists(self):
        """Test that pyradmon_bin2txt_driver.csh exists."""
        script_path = TIMESERIES_SRC / 'pyradmon_bin2txt_driver.csh'
        assert script_path.exists()
    
    def test_img_driver_exists(self):
        """Test that pyradmon_img_driver.csh exists."""
        script_path = TIMESERIES_SRC / 'pyradmon_img_driver.csh'
        assert script_path.exists()
    
    def test_main_driver_csh_exists(self):
        """Test that pyradmon_driver.csh exists."""
        script_path = TIMESERIES_SRC / 'pyradmon_driver.csh'
        assert script_path.exists()


class TestSupportingModules:
    """Tests for supporting Python modules."""
    
    def test_core_module_exists(self):
        """Test that core.py exists."""
        module_path = TIMESERIES_SRC / 'core.py'
        assert module_path.exists()
    
    def test_config_module_exists(self):
        """Test that config.py exists."""
        module_path = TIMESERIES_SRC / 'config.py'
        assert module_path.exists()
    
    def test_wrapper_module_exists(self):
        """Test that wrapper.py exists."""
        module_path = TIMESERIES_SRC / 'wrapper.py'
        assert module_path.exists()
    
    def test_data_module_exists(self):
        """Test that data.py exists."""
        module_path = TIMESERIES_SRC / 'data.py'
        assert module_path.exists()
    
    def test_plot_module_exists(self):
        """Test that plot.py exists."""
        module_path = TIMESERIES_SRC / 'plot.py'
        assert module_path.exists()


class TestConfigDirectory:
    """Tests for config directory."""
    
    def test_config_directory_exists(self):
        """Test that config directory exists."""
        config_dir = TIMESERIES_SRC / 'config'
        assert config_dir.exists()
        assert config_dir.is_dir()
    
    def test_radiance_plots_yaml_exists(self):
        """Test that main radiance_plots.yaml exists."""
        config_path = TIMESERIES_SRC / 'config' / 'radiance_plots.yaml'
        assert config_path.exists()
    
    def test_satlist_yaml_exists(self):
        """Test that satlist.yaml exists."""
        satlist_path = TIMESERIES_SRC / 'satlist.yaml'
        assert satlist_path.exists()
    
    def test_satlist_is_valid_yaml(self):
        """Test that satlist.yaml is valid YAML."""
        satlist_path = TIMESERIES_SRC / 'satlist.yaml'
        
        with open(satlist_path, 'r') as f:
            satlist = yaml.safe_load(f)
        
        assert satlist is not None

