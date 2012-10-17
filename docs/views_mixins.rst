Views Mixins
===========

DetailViewWithPostAction
------------------------

This view enhances the class-based generic detail view with even more generic post actions.
In order to use it, import it like all the other generic class based views and view mixins.

* Create a Mixin or View which inherits from this action mixin.
* Be sure to add a general ``get_success_url()`` function or custom success functions for each post action.
* Create your post actions
* Make sure to add this action names to the name attribute of an input field.


Basic usage in a html template::

    <form method="post" action=".">
		{% csrf_token %}
		<input name="post_verify" type="submit" value="Verify" />
	</form>


Usage in a views.py::

	from django_libs.views_mixins import DetailViewWithPostAction

    class NewsDetailMixin(DetailViewWithPostAction):
		"""
		Mixin to handle verify/reject processes.
	
		"""
		def post_verify(self):
			self.object.is_verified = True
			self.object.save()
	
		def post_reject(self):
			self.object.is_verified = False
			self.object.save()


	class NewsEntryDetailView(NewsDetailMixin):
		model = NewsEntry
	
		def get_success_url(self):
			return reverse('newsentry_detail', kwargs={'pk': self.object.pk})
	
		def post_verify(self):
			super(NewsEntryDetailView, self).post_verify()
			ctx_dict = {
				'verified': True,
				'entry': self.object,
			}
			self.send_mail_to_editor(ctx_dict)

		def get_success_url_post_reject(self):
			return reverse('newsentry_list')


JSONResponseMixin
-----------------

You can find out more about the ``JSONResponseMixin`` in the official Django
docs: https://docs.djangoproject.com/en/dev/topics/class-based-views/#more-than-just-html

In order to use it, just import it like all the other generic class based views
and view mixins::

    from django.views.generic import View
    from django_libs.views_mixins import JSONResponseMixin

    class MyAPIView(JSONResponseMixin, View):
        pass
