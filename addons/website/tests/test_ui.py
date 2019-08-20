# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

import eagle
import eagle.tests


@eagle.tests.tagged('-at_install', 'post_install')
class TestUiHtmlEditor(eagle.tests.HttpCase):
    def test_html_editor_multiple_templates(self):
        Website = self.env['website']
        View = self.env['ir.ui.view']
        generic_aboutus = Website.viewref('website.aboutus')
        # Use an empty page layout with oe_structure id for this test
        oe_structure_layout = '''
            <t name="About us" t-name="website.aboutus">
                <t t-call="website.layout">
                    <p>aboutus</p>
                    <div id="oe_structure_test_ui" class="oe_structure oe_empty"/>
                </t>
            </t>
        '''
        generic_aboutus.arch = oe_structure_layout
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('html_editor_multiple_templates')", "eagle.__DEBUG__.services['web_tour.tour'].tours.html_editor_multiple_templates.ready", login='admin')
        self.assertEqual(View.search_count([('key', '=', 'website.aboutus')]), 2, "Aboutus view should have been COW'd")
        self.assertTrue(generic_aboutus.arch == oe_structure_layout, "Generic Aboutus view should be untouched")
        self.assertEqual(len(generic_aboutus.inherit_children_ids.filtered(lambda v: 'oe_structure' in v.name)), 0, "oe_structure view should have been deleted when aboutus was COW")
        specific_aboutus = Website.with_context(website_id=1).viewref('website.aboutus')
        self.assertTrue(specific_aboutus.arch != oe_structure_layout, "Specific Aboutus view should have been changed")
        self.assertEqual(len(specific_aboutus.inherit_children_ids.filtered(lambda v: 'oe_structure' in v.name)), 1, "oe_structure view should have been created on the specific tree")

    def test_html_editor_scss(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('test_html_editor_scss')", "eagle.__DEBUG__.services['web_tour.tour'].tours.test_html_editor_scss.ready", login='admin')


class TestUiTranslate(eagle.tests.HttpCase):
    def test_admin_tour_rte_translator(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('rte_translator')", "eagle.__DEBUG__.services['web_tour.tour'].tours.rte_translator.ready", login='admin', timeout=120)


@eagle.tests.common.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):

    def test_01_public_homepage(self):
        self.phantom_js("/", "console.log('ok')", "'website.content.snippets.animation' in eagle.__DEBUG__.services")

    def test_02_admin_tour_banner(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('banner')", "eagle.__DEBUG__.services['web_tour.tour'].tours.banner.ready", login='admin')
