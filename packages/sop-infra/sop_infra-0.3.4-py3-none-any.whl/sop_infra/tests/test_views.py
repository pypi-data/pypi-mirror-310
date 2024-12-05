from django.urls import reverse

from utilities.testing import TestCase
from dcim.models import Site

from sop_infra.models import SopInfra


__all__ = (
    'SopInfraViewTestCase',
)


VIEW_PERM = 'sop_infra.view_sopinfra'
ADD_PERM = 'sop_infra.add_sopinfra'
EDIT_PERM = 'sop_infra.change_sopinfra'


class SopInfraViewTestCase(TestCase):

    user_permissions = ()

    @classmethod
    def setUpTestData(cls):

        sites = (
            Site(name='site 1', slug='site-1', status='active'),
            Site(name='site 2', slug='site-2', status='retired'),
        )
        for site in sites:
            site.full_clean()
            site.save()


    def get_action_url(self, action, instance=None):
        """reverse sopinfra plugin url with action"""
        url = f'plugins:sop_infra:sopinfra_{action}'

        if instance is None:
            return reverse(url)

        return reverse(url, kwargs={'pk': instance.pk})


    def test_list_no_perm(self):
        """test list view no perm"""
        url = self.get_action_url('list')

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)


    def test_list_perm(self):
        """test list view perm"""
        url = self.get_action_url('list')

        self.add_permissions(VIEW_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)


    def test_add_no_perm(self):
        """test add view no perm"""
        url = self.get_action_url('add')

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)


    def test_add_perm(self):
        """test add view perm"""
        url = self.get_action_url('add')

        self.add_permissions(ADD_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)


    def test_detail_no_perm(self):
        """test detail no perm"""
        instance = SopInfra.objects.first()
        url = self.get_action_url('detail', instance)

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)


    def test_detail_perm(self):
        """test detail perm"""
        instance = SopInfra.objects.first()
        url = self.get_action_url('detail', instance)

        self.add_permissions(VIEW_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)


    def test_edit_no_perm(self):
        """test edit no perm"""
        instance = SopInfra.objects.first()
        url = self.get_action_url('edit', instance)

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)


    def test_edit_perm(self):
        """test detail perm"""
        instance = SopInfra.objects.first()
        url = self.get_action_url('edit', instance)

        self.add_permissions(EDIT_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)


    def test_tab_view_no_perm(self):
        """test tab no perm"""
        instance = Site.objects.first()
        url = f'/dcim/sites/{instance.pk}/infra/'

        self.add_permissions('dcim.view_site')
        response = self.client.get(url)
        self.assertHttpStatus(response, 403)


    def test_tab_view_perm(self):
        """test tab perm"""
        instance = Site.objects.first()
        url = f'/dcim/sites/{instance.pk}/infra/'

        self.add_permissions('dcim.view_site')
        self.add_permissions(VIEW_PERM)
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)


    def test_tab_view_context(self):
        """test tab view context"""
        site = Site.objects.first()
        infra = SopInfra.objects.get(site=site)
        url = f'/dcim/sites/{site.pk}/infra/'
        s_ids = {}
        i_ids = {}

        for i in range(3):
            s = Site.objects.create(name=f'salut{i}', slug=f'salut{i}')
            s.full_clean()
            s.save()
            s_ids[i] = s.pk
            t = SopInfra.objects.get(site__id=s_ids[i])
            t.master_site=site
            t.full_clean()
            t.save()
            i_ids[i] = t.pk

        self.add_permissions('dcim.view_site')
        self.add_permissions(VIEW_PERM)
        response = self.client.get(url)
        context = response.context['context']

        self.assertHttpStatus(response, 200)
        self.assertEqual(context['sop_infra'], infra)
        self.assertEqual(context['count_slave_infra'], 3)
        self.assertEqual(context['count_slave'], 3)
        self.assertEqual(context['slave'], f'id={s_ids[0]}&id={s_ids[1]}&id={s_ids[2]}')
        self.assertEqual(context['slave_infra'], f'id={i_ids[0]}&id={i_ids[1]}&id={i_ids[2]}')


    def test_recompute_sizing_no_perm(self):
        """test recompute sizing no perm"""
        instance = Site.objects.first()
        url = self.get_action_url('refresh')

        response = self.client.get(url)
        self.assertHttpStatus(response, 403)

        response = self.client.get(f'{url}?qs={instance.pk}')
        self.assertHttpStatus(response, 403)


    def test_recompute_sizing_perm(self):
        """test recompute sizing with perm"""
        instance = Site.objects.first()
        url = self.get_action_url('refresh')

        self.add_permissions(EDIT_PERM)
        response = self.client.get(f'{url}?qs={instance.pk}')
        self.assertHttpStatus(response, 200)

