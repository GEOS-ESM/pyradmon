"""Tests for the spatial driver."""

import pytest
from pathlib import Path
import sys
import yaml

# Add path for imports
REPO_ROOT = Path(__file__).parent.parent
SPATIAL_SRC = REPO_ROOT / 'offline' / 'spatial' / 'src'
sys.path.insert(0, str(SPATIAL_SRC))
sys.path.insert(0, str(REPO_ROOT / 'offline'))


class TestSpatialDriverImports:
    """Tests for spatial driver imports."""
    
    def test_can_import_driver_module(self):
        """Test that the spatial driver module can be imported."""
        from pyradmon_driver_spatial import PyRadmonBase
        assert PyRadmonBase is not None
    
    def test_pyradmon_base_is_class(self):
        """Test that PyRadmonBase is a class."""
        from pyradmon_driver_spatial import PyRadmonBase
        assert isinstance(PyRadmonBase, type)


class TestConfigFiles:
    """Tests for configuration files."""
    
    def test_geosfp_config_exists(self):
        """Test that test_config.geosfp.yaml exists."""
        config_path = SPATIAL_SRC / 'test_config.geosfp.yaml'
        assert config_path.exists()
    
    def test_geosit_config_exists(self):
        """Test that test_config.geosit.yaml exists."""
        config_path = SPATIAL_SRC / 'test_config.geosit.yaml'
        assert config_path.exists()
    
    def test_m21c_config_exists(self):
        """Test that test_config.m21c.yaml exists."""
        config_path = SPATIAL_SRC / 'test_config.m21c.yaml'
        assert config_path.exists()
    
    def test_config_is_valid_yaml(self):
        """Test that config files are valid YAML."""
        config_path = SPATIAL_SRC / 'test_config.geosfp.yaml'
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        assert isinstance(config, dict)
    
    def test_config_has_required_fields(self):
        """Test that config has required fields."""
        config_path = SPATIAL_SRC / 'test_config.geosfp.yaml'
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        required_fields = ['expver', 'yyyymmdd', 'hh']
        for field in required_fields:
            assert field in config, f"Missing required field: {field}"
    
    def test_config_obs_types_are_valid(self):
        """Test that observation type values are valid (0, 1, or 'on'/'off')."""
        config_path = SPATIAL_SRC / 'test_config.geosfp.yaml'
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        obs_types = ['atms', 'amsr2', 'amsua', 'avhrr', 'gmi', 
                     'hirs', 'mhs', 'seviri', 'ssmis', 'cris', 'airs', 'iasi']
        
        valid_values = [0, 1, 'on', 'off', 'On', 'Off', 'ON', 'OFF']
        
        for obs_type in obs_types:
            if obs_type in config:
                assert config[obs_type] in valid_values, \
                    f"Invalid value for {obs_type}: {config[obs_type]}"


class TestObservationScripts:
    """Tests for observation processing scripts."""
    
    @pytest.mark.parametrize("script_name", [
        "do_atms.csh",
        "do_amsr2.csh", 
        "do_amsua.csh",
        "do_avhrr.csh",
        "do_gmi.csh",
        "do_hirs.csh",
        "do_mhs.csh",
        "do_seviri.csh",
        "do_ssmis.csh",
        "do_cris.csh",
        "do_airs.csh",
        "do_iasi.csh",
    ])
    def test_observation_script_exists(self, script_name):
        """Test that observation processing scripts exist."""
        script_path = SPATIAL_SRC / script_name
        assert script_path.exists(), f"Missing script: {script_name}"


class TestUtilsModule:
    """Tests for utils module."""
    
    def test_logging_config_importable(self):
        """Test that logging_config module can be imported."""
        from utils.logging_config import setup_logging, get_logger
        assert setup_logging is not None
        assert get_logger is not None

