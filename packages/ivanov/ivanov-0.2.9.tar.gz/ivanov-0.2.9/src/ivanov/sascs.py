from .core import AbstractSAS
from .globals import sascs_sasobjsp_host, sascs_sasobjsp_port, sascs_workspace, sasvs235_sasobjsp_host, \
sasvs235_drkr_workspace, sasvs235_sasapp_workspace, sasvs235_drkr_pm_workspace, sasvs235_drkr_fdp_workspace, \
sasvs235_drkr_scu_workspace, sasvs235_drkr_rt_workspace, sasvs235_drkr_rwo_workspace, sasvs221_sasobjsp_host, \
sasvs221_sasobjsp_port, sasvs221_drkr_workspace, sasvs221_sasapp_workspace, sasvs221_dsur_workspace, \
sasvs221_dfpc_workspace, sasvs221_aso_workspace, sasvs235_sasobjsp_port


class SASCS(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host=sascs_sasobjsp_host,
                       sasobjsp_port=sascs_sasobjsp_port,
                       appserver=sascs_workspace,
                 **kwargs):
        self.platform = 'SASCS'
        self.env_type = 'Prod'
        super(SASCS, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                    **kwargs)

    def _is_appserver_valid(self, appsever):
        allowed_appservers = [sascs_workspace]
        for existing_appserver in allowed_appservers:
            if existing_appserver.lower().startswith(appsever.lower()):
                return appsever
        else:
            raise ValueError(f'Appserver must be one of: {allowed_appservers}')


class SASScoringVS235(AbstractSAS):
    def __init__(self, user,
                         password,
                         sasobjsp_host=sasvs235_sasobjsp_host,
                         sasobjsp_port=sasvs235_sasobjsp_port,
                         appserver=sasvs235_drkr_workspace,
                 **kwargs):
        self.platform = 'SASScoringVS235'
        self.env_type = 'Prod'
        super(SASScoringVS235, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                    **kwargs)

    def _is_appserver_valid(self, appsever):
        allowed_appservers = [sasvs235_drkr_workspace, sasvs235_sasapp_workspace, sasvs235_drkr_pm_workspace,
                              sasvs235_drkr_fdp_workspace, sasvs235_drkr_scu_workspace, sasvs235_drkr_rt_workspace,
                              sasvs235_drkr_rwo_workspace]
        for existing_appserver in allowed_appservers:
            if existing_appserver.lower().startswith(appsever.lower()):
                return appsever
        else:
            raise ValueError(f'Appserver must be one of: {allowed_appservers}')


class SASScoringVS221(AbstractSAS):
    def __init__(self, user,
                         password,
                         sasobjsp_host=sasvs221_sasobjsp_host,
                         sasobjsp_port=sasvs221_sasobjsp_port,
                         appserver=sasvs221_dfpc_workspace,
                 **kwargs):
        self.platform = 'SASScoringVS221'
        self.env_type = 'Pre-prod'
        super(SASScoringVS221, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password,
                                    appserver=self._is_appserver_valid(appserver),
                                              **kwargs)

    def _is_appserver_valid(self, appsever):
        allowed_appservers = [sasvs221_sasapp_workspace, sasvs221_dsur_workspace, sasvs221_dfpc_workspace,
                              sasvs221_aso_workspace, sasvs221_drkr_workspace]
        for existing_appserver in allowed_appservers:
            if existing_appserver.lower().startswith(appsever.lower()):
                return appsever
        else:
            raise ValueError(f'Appserver must be one of: {allowed_appservers}')
