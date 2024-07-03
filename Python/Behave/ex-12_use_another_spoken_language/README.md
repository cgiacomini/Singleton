
Goal:	Use another spoken language for testing (other than English)
Most BDD frameworks provide internationalisation support. The key part (but only the first step) is that the Given ... When ... Then keywords are provided in the native language, for example French or German. If this is the case, a developer can provide step definitions in another spoken language.

Hint

The list of supported languages can be displayed via:

behave --lang-list
Feature files can be tagged for a specific language, like:

# language: de
# -- file:*.feature
...
When this happens, the BDD framework selects the keywords for this language. The default language can be defined in the configuration file. behave uses either behave.ini or .behaverc as configuration file:

# -- file:behave.ini
[behave]
lang = de
