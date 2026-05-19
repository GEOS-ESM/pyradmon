import matplotlib
matplotlib.use('Agg')
import ncdiag as ncd
import yaml
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

print('matplotlib version')
print(matplotlib.__version__)

# added format for chinfo 20210307 - still something going on with some ch. 1 plots
# added use of 'Agg' 20210307 - this results in much speedier production of plots
# implemented plot.close() 20210307 - this resolved memory errors
# 
# Will added new coolwarm colorbar and capability to center colorbar and to set max/min
# 20210317 changes made to all 4 yaml files and pyradmon_spatial.py

class pyradmon_spatial():

    def setup_subst_dict(self,var=None):
        import pretty_satsen as pss
        import gmao_tools as gt

        dt = gt.ndate_to_dt(int(self.data.global_attr('date_time')))

        subst = {
            'sensat':     self.data.global_attr('Satellite_Sensor'),
            'ndate':      self.data.global_attr('date_time'),
            'ch':         self.current_chan,
            'chinfo':     self.get_pretty_chinfo(),
            'sensor':     self.data.global_attr('Observation_type'),
            'satellite':  self.data.global_attr('Satellite'),
            'psensor':    pss.sensor[self.data.global_attr('Observation_type')] if (self.data.global_attr('Observation_type') in pss.sensor) else self.data.global_attr('Observation_type'),
            'psatellite': pss.satellite[self.data.global_attr('Satellite')] if (self.data.global_attr('Satellite') in pss.satellite) else self.data.global_attr('Satellite'),
            'year':       dt.strftime("%Y"),
            'mon':        dt.strftime("%m"),
            'shortmon':   dt.strftime("%b"),
            'fullmon':    dt.strftime("%B"),
            'day':        dt.strftime("%d"),
            'hour':       dt.strftime("%H"),
        }    
        print(f'---- var: {var}')
        if var is not None:
            subst.update({
                'nobs':  var.size,
                'avg':   '{:0.2f}'.format(np.mean(var)),
                'std':   '{:0.2f}'.format(np.std(var)),
            })

        return(subst)                
#avg=avg,std=std,chinfo=chinfo,ch=self.current_chan,nobs=nobs,
#                                                  sensat=self.data.global_attr('Satellite_Sensor'),ndate=self.data.global_attr('date_time'))
#            avg  = '{:.2f}'.format(np.mean(self.data.v(cfg['var'])))
#            std  = '{:.2f}'.format(np.std(self.data.v(cfg['var'])))
#            if self.frequency[self.current_chan-1] < 1000:
#                chinfo = '{:.3f} GHz'.format(self.frequency[self.current_chan-1])
#            else:
#                chinfo = '{} cm-1'.format(self.wavenumber[self.current_chan-1])

    def get_pretty_chinfo(self):
        if self.frequency[self.current_chan-1] < 1000:
            chinfo = '{:.3f} GHz'.format(self.frequency[self.current_chan-1])
        else:
            chinfo = '{:.3f} cm$^-$$^1$'.format(self.wavenumber[self.current_chan-1])
        return(chinfo)

    def __init__(self,datafn,configfn,show=True,save=False):

        self.datafile=datafn
        self.configfile=configfn

        print('Input data diag: %s' % self.datafile)
        print('Input config file: %s' % self.configfile)
 
        self.data=ncd.obs(self.datafile)
        self.frequency=self.data.v('frequency')
        self.wavenumber=self.data.v('wavenumber')
        self.config=yaml.load(open(self.configfile), Loader=yaml.SafeLoader)
#        self.config=yaml.load(open(self.configfile))
# updated 20201004 - A. Conaty per a depracation warning
# https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
#
        self.show_plot=show
        self.save_plot=save
        self.curax=None

    def plot_init(self,cfg):
#        if 'figsize' in self.config['plot_config']:
#        try:
#            plt.rcParams.update({'font.size': self.config['plot_config']['fontsize']})
#        except:
#            plt.rcParams.update({'font.size': 22})
# 
#        try:
#            figsize=self.config['plot_config']['figsize']
#        except:
#            figsize=(7,5)
#        for rcp in self.config['plot_config']:
#            plt.rcParams.update({ rcp: self.config['plot_config'][rcp] })

        self.transform=ccrs.PlateCarree()
        self.curfig, self.curax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
#        self.curax = plt.axes(projection=self.transform)
        self.curax.coastlines()

    def plot_data(self,cfg):
        from string import Template
        from matplotlib.colors import TwoSlopeNorm
        import matplotlib.colors as mcolors

        try:
            sz = cfg['markersize']
        except:
            sz = None 

        nobs = self.data.v('lon').size
        subst = self.setup_subst_dict(var=self.data.v(cfg['var']))

        #print(f' ------ cfg: {print(cfg)} --------------')
        cbar_min = None
        cbar_max = None
        norm = None
        if 'cbar_min' in cfg:
            cbar_min = cfg['cbar_min']
        if 'cbar_max' in cfg:
            cbar_max = cfg['cbar_max']
        if 'cbar_style' in cfg:
            if cfg['cbar_style'] == 'centerzero':
                vcenter = 0.0
                #norm = TwoSlopeNorm(vcenter=vcenter)
                norm = TwoSlopeNorm(vmin=cbar_min, vmax=cbar_max, vcenter=vcenter) #
                #norm = mcolors.DivergingNorm(vmin=cbar_min,vmax=cbar_max,vcenter=vcenter)
                """
                import matplotlib as mpl
                norm = mpl.colors.Normalize(vmin=-1, vmax=1)
                norm(0)
                """

        print(f' ------------- cbar_min:{cbar_min} , cbar_max:{cbar_max} , norm:{norm} --------------')


        if (nobs <= 0):
            cs = None 
            self.curax.text(0.5,0.5,'No Data', horizontalalignment='center',verticalalignment='center',fontsize=20,color='red')#,transform=self.transform)
            if 'cbar_title' in cfg:
#                cbtitle = Template(cfg['cbar_title'])
#                cbtitle = cbtitle.safe_substitute(avg='n/a',std='n/a',chinfo=chinfo,ch=self.current_chan,nobs=nobs)
                cbtitle = Template(cfg['cbar_title'])
                cbtitle = cbtitle.safe_substitute(subst)


        else:
            print(f' ------ vmin=cbar_min,vmax=cbar_max,norm=norm {cbar_min} , {cbar_max} , {norm} --------------')
            cs = self.curax.scatter(self.data.v('lon'),self.data.v('lat'),
                                   c=self.data.v(cfg['var']),
                                   linewidths=0,s=sz,
                                   transform=self.transform,
                                   vmin=cbar_min,vmax=cbar_max, 
                                   #norm=norm,
                                   cmap=cfg['cmap']
                                   )
            #print(f' ------ self.data: {self.data} --------------')
            avg  = '{:f}'.format(np.mean(self.data.v(cfg['var'])))
            std  = '{:f}'.format(np.std(self.data.v(cfg['var'])))
            if self.frequency[self.current_chan-1] < 1000:
                chinfo = '{:0.3f} GHz'.format(self.frequency[self.current_chan-1])
            else:
                chinfo = '{} cm-1'.format(self.wavenumber[self.current_chan-1])

            cbtitle = ''
            if 'cbar_title' in cfg:
#                cbtitle = Template(cfg['cbar_title'])
#                cbtitle = cbtitle.safe_substitute(avg=avg,std=std,chinfo=chinfo,ch=self.current_chan,nobs=nobs,
#                                                  sensat=self.data.global_attr('Satellite_Sensor'),ndate=self.data.global_attr('date_time'))
                cbtitle = Template(cfg['cbar_title']).safe_substitute(subst)                
            cb = self.curfig.colorbar(cs,orientation='horizontal',pad=0.0,shrink=0.9)
            cb.set_label(cbtitle)

        plttitle = ''
        if 'plot_title' in cfg:
            plttitle = Template(cfg['plot_title'])
            plttitle = plttitle.safe_substitute(subst)
#avg=avg,std=std,chinfo=chinfo,ch=self.current_chan,nobs=nobs,
#                                                  sensat=self.data.global_attr('Satellite_Sensor'),ndate=self.data.global_attr('date_time'))
        self.curax.set_title(plttitle)

    def plot_finalize(self,cfg):
        from string import Template

        subst = self.setup_subst_dict()

# Moved by Will's recommendation
#        plt.tight_layout()

        for rcp in self.config['plot_config']['rcparams']:
            plt.rcParams.update({ rcp: self.config['plot_config']['rcparams'][rcp] })

        self.curax.set_xlim(self.config['plot_config']['xrange'])
        self.curax.set_ylim(self.config['plot_config']['yrange'])

        plt.tight_layout()

        if (self.save_plot):
            try:
               fn = Template(cfg['filename'])
            except:
               print('Warning - no filename given, using output.png')
               fn = Template('output.png')
            fn = fn.safe_substitute(subst)
            plt.savefig(fn)
                        
        if (self.show_plot):
            plt.show()
#will's recommended close
        plt.close()
        self.curfig= None
        self.curax = None

    def generate_plots(self):
        for cplot_name in self.config['plots']:
             cplot = self.config['plots'][cplot_name]
             print(cplot['chan'])
             self.data.use_mask(False)
             if (cplot['chan'] == 'all'):
                 chans = [i+1 for i, x in enumerate(self.data.v('use_flag'))]
             elif (cplot['chan'] == 'used'):
                 chans = [i+1 for i, x in enumerate(self.data.v('use_flag')) if x > 0]
             else:
                 try:
                     chans = [cplot['chan']]
                 except:
                     raise Exception('unexpected value for chan in {}'.format(cplot))

             for cc in chans:
                 cmask = cplot['mask'] + ' & (Channel_Index == {})'.format(cc)
                 print(cmask)
                 self.current_chan = cc
                 self.data.set_mask(cmask)
                 self.data.use_mask(True)

                 self.plot_init(cplot)
                 self.plot_data(cplot)
                 self.plot_finalize(cplot)

