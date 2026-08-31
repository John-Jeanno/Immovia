from django.test import SimpleTestCase
from importlib import import_module


class DashboardTemplateTest(SimpleTestCase):
    def test_dashboard_template_exists(self):
        view_module = import_module('views')
        self.assertTrue(hasattr(view_module, 'DashboardView'))
        self.assertIn(view_module.DashboardView.template_name, {'dashboard.html', 'index.html'})
