from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, \
    SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from backend.apps.alarms.views import DeviceAlarmLogsViewSet
from backend.apps.configuration_cfgs.views import DeviceAttrVariableViewSet, ApiVariableViewSet, \
    FrontCustomVariableViewSet
from backend.apps.custom_reqlogs.views import CustomRequestLogsViewSets
from backend.apps.custom_servers.views import DomainView
from backend.apps.air_servers.views import AirCondGroupViewSet, CentralAirConditionerViewSet,  \
    AirPersonnelSensorViewSet, AirSpaceTightSensorViewSet
from backend.apps.device_models.views import AirCondViewSet, PersonnelSensorViewSet, \
    SpaceTightSensorViewSet, DeviceModelView, ElectricMeterViewSet, \
    IotBreakerViewSet, PowerSourceViewSet, HiddenDangerMonitorViewSet, \
    ElMonitorInstrumentViewSet, TransformerViewSet, \
    TfTemperatureMonitorViewSet, LightMonitorViewSet, SwitchMonitorViewSet, EnvironmentMonitorViewSet, \
    PrepaidElectricMeterViewSet
from backend.apps.el_branch.views import BranchTreeNodeViewSet, ElInstrumentViewSet
from backend.apps.el_energy_signboards.views import ElHiddenDangerMonitorViewSet, ElPowerSourceViewSet, \
    ElectricMeterLoadViewSet
from backend.apps.el_prepayment_servers.views import PrepaidOrgCfgViewSet, PrepaidElMeterViewSet, TenantElMeterViewSet, \
    TenantRechargeRecordViewSet, RechargeRecordViewSet, MeterReadRecordViewSet, EventRecordViewSet, \
    WithdrawalRecordsViewSet, ElDailyStatisticViewSet, RechargeOrderViewSet, PrepaidElMeterGroupViewSet, \
    OrgPriceCfgViewSet, WechatPayNotifyView
from backend.apps.energy_statistics.views import StatisticDimensionViewSet, DimensionNodeViewSet, \
    ElectricMeterNodeViewSet
from backend.apps.energy_waste_statistics.views import EnergyWasteGroupViewSet, EnergyWasteDeviceViewSet, \
    EnergyWasteDailyDataViewSet
from backend.apps.environment_monitor.views import EnvironmentMonitorNodeViewSet, EnvironmentDeviceViewSet, \
    EnvDistributionViewSet
from backend.apps.equipments.views import ISWDataView, EZtProjectsView, \
    DeviceCategoryViewSet, DeviceViewSet, CategoryModeMappingViewSet, DeviceSyncRecordViewSet, \
    DeviceAttrDataViewSet, DeviceControlLoggingViewSet
from backend.apps.iot_breakers.views import IotBreakerTreeNodeViewSet, IotBreakerDeviceViewSet
from backend.apps.lighting_monitor.views import LightMonitorNodeViewSet, LightDeviceViewSet
from backend.apps.proj_common.views import ConstDataAPI
from backend.apps.projects.views import ProjectViewSet, OrgTreeViewSet, \
    ProjectMemberViewSet, ProjectsAppMenusViewSet, OrgAppMenusViewSet, ProjectGroupViewSet
from backend.apps.scenes.views import SceneConfigViewSet
from backend.apps.switch_monitor.views import SwitchMonitorNodeViewSet, SwitchDeviceViewSet
from backend.apps.transformer_monitor.views import TransformerMonitorViewSet
from backend.apps.uploader.views import UploadViewSet
from backend.apps.users.views import ErrorTimesView, UserViewSet, ExtraLogin, \
    ImageCaptchaView, RegisterViewSet
from backend.apps.iam_client.urls import iam_client_urls


# 系统级 路由
router = routers.DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('projects', ProjectViewSet, 'projects')
router.register('uploader', UploadViewSet, 'uploader')
router.register('ezt_datas', ISWDataView, 'ezt_datas')
router.register('device_models', DeviceModelView, 'device_models')
router.register('register', RegisterViewSet, 'register')
router.register('tenant_el_meters', TenantElMeterViewSet, 'tenant_el_meters')
router.register('tenant_recharge_records', TenantRechargeRecordViewSet, 'tenant_recharge_records')
router.register('tenant_recharge_orders', RechargeOrderViewSet, 'tenant_recharge_orders')
router.register('request_logs', CustomRequestLogsViewSets, 'request_logs')

# 项目级 路由
project_router = routers.DefaultRouter()
project_router.register('orgs', OrgTreeViewSet, 'orgs')
project_router.register('app_menus', ProjectsAppMenusViewSet, 'app_menus')
project_router.register('project_members', ProjectMemberViewSet, 'project_members')
project_router.register('ezt_projects', EZtProjectsView, 'ezt_projects')
project_router.register('device_category', DeviceCategoryViewSet, 'device_category')
project_router.register('category_mode_mapping', CategoryModeMappingViewSet, 'category_mode_mapping')
project_router.register('devices', DeviceViewSet, 'devices')
project_router.register('air_cond_groups', AirCondGroupViewSet, 'air_cond_groups')
project_router.register('central_air_cond', CentralAirConditionerViewSet, 'central_air_cond')
project_router.register('air_personnel_sensors', AirPersonnelSensorViewSet, 'air_personnel_sensors')
project_router.register('air_space_tight_sensors', AirSpaceTightSensorViewSet, 'air_space_tight_sensors')
project_router.register('air_conds', AirCondViewSet, 'air_conds')
project_router.register('personnel_sensors', PersonnelSensorViewSet, 'personnel_sensors')
project_router.register('space_tight_sensors', SpaceTightSensorViewSet, 'space_tight_sensors')
project_router.register('electric_meters', ElectricMeterViewSet, 'electric_meters')
project_router.register('stat_dimensions', StatisticDimensionViewSet, 'stat_dimensions')
project_router.register('dimension_nodes', DimensionNodeViewSet, 'dimension_nodes')
project_router.register('node_electric_meters', ElectricMeterNodeViewSet, 'node_electric_meters')

# RESTful 风格的路由
restful_project_router = routers.DefaultRouter()
restful_project_router.register('orgs', OrgTreeViewSet, 'restful_orgs')
restful_project_router.register('app_menus', ProjectsAppMenusViewSet, 'restful_app_menus')
restful_project_router.register('project_members', ProjectMemberViewSet, 'restful_project_members')
restful_project_router.register('ezt_projects', EZtProjectsView, 'restful_ezt_projects')
restful_project_router.register('device_category', DeviceCategoryViewSet, 'restful_device_category')
restful_project_router.register('category_mode_mapping', CategoryModeMappingViewSet, 'restful_category_mode_mapping')
restful_project_router.register('devices', DeviceViewSet, 'restful_devices')
restful_project_router.register('air_cond_groups', AirCondGroupViewSet, 'restful_air_cond_groups')
restful_project_router.register('central_air_cond', CentralAirConditionerViewSet, 'restful_central_air_cond')
restful_project_router.register('air_personnel_sensors', AirPersonnelSensorViewSet, 'restful_air_personnel_sensors')
restful_project_router.register('air_space_tight_sensors', AirSpaceTightSensorViewSet, 'restful_air_space_tight_sensors')
restful_project_router.register('air_conds', AirCondViewSet, 'restful_air_conds')
restful_project_router.register('personnel_sensors', PersonnelSensorViewSet, 'restful_personnel_sensors')
restful_project_router.register('space_tight_sensors', SpaceTightSensorViewSet, 'restful_space_tight_sensors')
restful_project_router.register('electric_meters', ElectricMeterViewSet, 'restful_electric_meters')
restful_project_router.register('stat_dimensions', StatisticDimensionViewSet, 'restful_stat_dimensions')
restful_project_router.register('dimension_nodes', DimensionNodeViewSet, 'restful_dimension_nodes')
restful_project_router.register('node_electric_meters', ElectricMeterNodeViewSet, 'restful_node_electric_meters')
restful_project_router.register('iot_breakers', IotBreakerViewSet, 'iot_breakers')
restful_project_router.register('iot_breaker_trees', IotBreakerTreeNodeViewSet, 'iot_breaker_trees')
restful_project_router.register('iot_breaker_devices', IotBreakerDeviceViewSet, 'iot_breaker_devices')
restful_project_router.register('power_sources', PowerSourceViewSet, 'power_sources')
restful_project_router.register('hidden_danger_monitors', HiddenDangerMonitorViewSet, 'hidden_danger_monitors')
restful_project_router.register('el_hidden_danger_monitors', ElHiddenDangerMonitorViewSet, 'el_hidden_danger_monitors')
restful_project_router.register('el_power_sources', ElPowerSourceViewSet, 'el_power_sources')
restful_project_router.register('el_meter_loads', ElectricMeterLoadViewSet, 'el_meter_loads')
restful_project_router.register('alarm_logs', DeviceAlarmLogsViewSet, 'alarm_logs')
restful_project_router.register('el_instruments', ElMonitorInstrumentViewSet, 'el_instruments')
restful_project_router.register('branch_tree_nodes', BranchTreeNodeViewSet, 'branch_tree_nodes')
restful_project_router.register('branch_el_instruments', ElInstrumentViewSet, 'branch_el_instruments')
restful_project_router.register('transformers', TransformerViewSet, 'transformers')
restful_project_router.register('t_temperature_monitors', TfTemperatureMonitorViewSet, 't_temperature_monitors')
restful_project_router.register('transformer_monitors', TransformerMonitorViewSet, 'transformer_monitors')
restful_project_router.register('org_app_menus', OrgAppMenusViewSet, 'restful_org_app_menus')
restful_project_router.register('device_datas', DeviceAttrDataViewSet, 'device_datas')
restful_project_router.register('groups', ProjectGroupViewSet, 'groups')
restful_project_router.register('device_sync_records', DeviceSyncRecordViewSet, 'device_sync_records')
restful_project_router.register('light_monitors', LightMonitorViewSet, 'light_monitors')
restful_project_router.register('light_monitor_nodes', LightMonitorNodeViewSet, 'light_monitor_nodes')
restful_project_router.register('light_devices', LightDeviceViewSet, 'light_devices')
restful_project_router.register('control_logs', DeviceControlLoggingViewSet, 'control_logs')
restful_project_router.register('switch_monitors', SwitchMonitorViewSet, 'switch_monitors')
restful_project_router.register('env_monitors', EnvironmentMonitorViewSet, 'env_monitors')
restful_project_router.register('env_monitor_nodes', EnvironmentMonitorNodeViewSet, 'env_monitor_nodes')
restful_project_router.register('env_devices', EnvironmentDeviceViewSet, 'env_devices')
restful_project_router.register('env_distribution_maps', EnvDistributionViewSet, 'env_distribution_maps')
restful_project_router.register('switch_monitor_nodes', SwitchMonitorNodeViewSet, 'switch_monitor_nodes')
restful_project_router.register('switch_devices', SwitchDeviceViewSet, 'switch_devices')
restful_project_router.register('ew_groups', EnergyWasteGroupViewSet, 'ew_groups')
restful_project_router.register('ew_devices', EnergyWasteDeviceViewSet, 'ew_devices')
restful_project_router.register('ew_daily_datas', EnergyWasteDailyDataViewSet, 'ew_daily_datas')
restful_project_router.register('scenes', SceneConfigViewSet, 'scenes')
restful_project_router.register('p_el_meters', PrepaidElectricMeterViewSet, 'p_el_meters')

# 组织隔离api
restful_org_router = routers.DefaultRouter()
restful_org_router.register('el_meter_groups', PrepaidElMeterGroupViewSet, 'el_meter_groups')
restful_org_router.register('org_price_cfgs', OrgPriceCfgViewSet, 'org_price_cfgs')
restful_org_router.register('org_prepaid_cfgs', PrepaidOrgCfgViewSet, 'org_prepaid_cfgs')
restful_org_router.register('prepaid_el_meters', PrepaidElMeterViewSet, 'prepaid_el_meters')
restful_org_router.register('recharge_records', RechargeRecordViewSet, 'recharge_records')
restful_org_router.register('meter_read_records', MeterReadRecordViewSet, 'meter_read_records')
restful_org_router.register('event_records', EventRecordViewSet, 'event_records')
restful_org_router.register('withdrawal_records', WithdrawalRecordsViewSet, 'withdrawal_records')
restful_org_router.register('el_daily_statistics', ElDailyStatisticViewSet, 'el_daily_statistics')
restful_org_router.register('device_attr_variables', DeviceAttrVariableViewSet, 'device_attr_variables')
restful_org_router.register('api_variables', ApiVariableViewSet, 'api_variables')
restful_org_router.register('front_custom_variables', FrontCustomVariableViewSet, 'front_custom_variables')

api_v1 = [
    path('iam/', include((iam_client_urls, 'iam'), namespace="iam")),
]

urlpatterns = [
    re_path('^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_login/', ExtraLogin.as_view()),
    path('api/error_times/', ErrorTimesView.as_view(), name='error_times'),
    path('api/image_captcha/', ImageCaptchaView.as_view(), name='image_captcha'),
    path('api/const_data/', ConstDataAPI.as_view(), name='const_data'),
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/wechat/pay_notify_callback/', WechatPayNotifyView.as_view(), name='pay_notify_callback'),
    path('api/wechat/', include('backend.apps.wechat.urls')),
    path('api/yingshi/', include('backend.apps.yingshi.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include(router.urls)),
    path('api/domain/', DomainView.as_view(), name="domain"),
    path('api/projects/<str:project>/', include(restful_project_router.urls)),
    path('api/projects/<str:project>/orgs/<str:org>/', include(restful_org_router.urls)),
    path('api/v1/', include((api_v1, 'api_v1'), namespace="api_v1")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 文档相关路由
if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
else:
    urlpatterns += [
        path('api/schema/', cache_page(3600)(SpectacularAPIView.as_view()), name='schema'),
        path('swagger-ui/', cache_page(3600)(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
        path('redoc/', cache_page(3600)(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    ]

if settings.IS_USE_COS:
    from backend.apps.common.views import StsAuth, StsAuthToken
    def root_view(request):
        """根路径视图，返回简单的API信息"""
        return JsonResponse({
            'message': 'EZtView API Server',
            'version': '2.0',
            'status': 'running',
            'docs': '/swagger-ui/' if settings.DEBUG else None
        })
    urlpatterns += [
        path("", root_view, name="home"),
        path('api/sts-auth/', StsAuth.as_view(), name="sts-auth"),
        path('api/sts-auth-token/', StsAuthToken.as_view(), name="sts-auth"),
    ]
else:
    from django.views.generic import TemplateView
    urlpatterns += [
        path("", TemplateView.as_view(template_name="index.html"), name="home"),
    ]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
