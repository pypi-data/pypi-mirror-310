# audrius-m-mod1-atsiskaitymas

## You can install it with pip:
```
pip install audrius-m-mod1-atsiskaitymas
```

## And test like that
```
from audrius_m_mod1_atsiskaitymas.crawler import crawl

print(crawl(time_limit=60, source='https://lt.wikipedia.org/wiki/Pagrindinis_puslapis', return_format='text'))
```

## Pypi repository is here:
https://pypi.org/project/audrius-m-mod1-atsiskaitymas/

## run test coverage:
`pytest --cov=audrius_m_mod1_atsiskaitymas tests/`

## Sample run results are stored in sample_results/ folder

## Package and upload to pypi:
```
python setup.py sdist bdist_wheel

twine upload dist/*
```