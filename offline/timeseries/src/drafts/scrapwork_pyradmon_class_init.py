# Draft/Scrapwork ~ pyradmon_driver_offline.py
# Figuring out best way to create the main class

     #try:
            #self.scp_userhost = config['scp_userhost'] #
            #self.scp_path = config['scp_path'] #
        #
        #
        # attrs created from inputs
        self.ndstartdate = config['startdate'][:-4].replace(" ", "") #
        self.ndenddate = config['enddate'][:-4].replace(" ", "") #
        self.exprc = config_yaml_path
        self.rcfile = config_yaml_path
        bin2txtnl = os.path.join(self.pyradmon,'/gsidiag/gsidiag_bin2txt/gsidiag_bin2txt.nl')

        if config:
            self.pyradmon = config.get('pyradmon', self.default_value_a)
            self.variable_b = config.get('variable_b', self.default_value_b)
            self.variable_c = config.get('variable_c', self.default_value_c)
            self.pyradmon = config['pyradmon'] #/home/dao_ops/pyradmon/
            self.arcbase = config['arcbase'] #/home/dao_ops/m21c/archive/
            self.data_dirbase = os.path.join(self.arcbase, self.expid, 'obs') #config['data_dirbase'] #/home/dao_ops/m21c/archive/e5303_m21c_jan18/obs
            self.runbase = os.path.join([self.arcbase, self.expid, 'obs']) #config['runbase']
            self.expbase = config['expbase'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/
            self.scratch_dir = config['scratch_dir'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/scratch
            self.output_dir = config['output_dir'] #/discover/nobackup/projects/gmao/r21c/aelakkra/TBR/radmon/time_series/m21c_radmon/radmon
            self.gsidiagsrc = config['gsidiagsrc']
            #optional
            #########
            self.mstorage = config['mstorage'] #
            #self.instruments = config['instruments'] #
            self.bin2txt_exec = config['bin2txt_exec'] #
            self.bin2txt_nl = config['bin2txt_nl'] #
                        # attrs created from inputs
            self.ndstartdate = config['startdate'][:-4].replace(" ", "") #
            self.ndenddate = config['enddate'][:-4].replace(" ", "") #
            self.exprc = config_yaml_path
            self.rcfile = config_yaml_path
        else:
             self.variable_a = self.default_value_a
             self.variable_b = self.default_value_b
             self.variable_c = self.default_value_c


        def __repr__(self):
            return f"Person(name='{self.name}', age={self.age}, city='{self.city}')"

        # pyradmon_bin2txt_driver while loop line 74 equivalent
        def config_overide(config_yaml_path):
     
        def add_attribute(self, name, value):
            setattr(self, name, value)

        def get_attribute(self, name):
            return getattr(self, name)