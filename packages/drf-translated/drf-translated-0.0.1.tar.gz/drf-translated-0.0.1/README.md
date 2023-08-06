# drf-translated 

django-modeltranslation DRF serializers

## Features

- Query/context translation support
- Highly customizable

## Installation 
```bash
pip install drf-translated
```

## Usage

Create a drf_translated.serializers.TranslatedModelSerializer serializer for your registered translation model:

```python
from drf_translated.serializers import TranslatedModelSerializer

class MovieSerializer(TranslatedModelSerializer):
  class Meta:
    model = Movie

    fields = '__all__'

```

| Setting | Default | Description |
| ------ | ------ | ------ |
| DRF_TRANSLATED_QUERY_PARAM | language | Query language param to convert translated values from dict to str |
| DRF_TRANSLATED_LOCALE_CONTEXT | locale | Serializer context key for getting translation language |
