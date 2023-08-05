import factory
from factory.django import DjangoModelFactory as FBDjangoModelFactory

class DjangoModelFactory(FBDjangoModelFactory):
    @staticmethod
    def create_post_generated_subfactory(field, Factory):
        def post_generation_function(obj, create, extracted, count=0, **kwargs):
            base_creation_kwargs = {field.remote_field.name: obj}
            if extracted:
                for extracted_info in extracted:
                    Factory(**extracted_info, **base_creation_kwargs)
            elif count:
                for _ in range(count):
                    Factory(**base_creation_kwargs)

        return factory.post_generation(post_generation_function)