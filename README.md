# Parse Wiktionary

Wiktionary.org is a masterpiece of human collaboration. It tries to provide a definition and description of every word from all languages. And they do so under the _Creative Commons Attribution-ShareAlike 3.0 Unported License_ and _GNU Free Documentation License_.

The project is a wonderful endeavour from the Wikimedia Foundation (the same Foundation which runs Wikipedia), but it comes with one major caveat for developers: it doesn't offer a straight-forward, free and unthrotteled API for people to use the massive information the platform has to offer.

But there is hope! Every few weeks, they scratch all their data together and export them as XML files. They are separated by the language of the Wiktionary Pages.

```
The aim of this project is to parse these Wiktionary Dumps and 
thereby enable developers to build cool language-based applications.
```



### Please make sure to use this table for every Merge Request you make
| commit    | message                                                             | 
|-----------|:--------------------------------------------------------------------|
| `feat`    | new feature for the user                                            |
| `fix`     | bug fix for the user                                                |
| `docs`    | changes to the documentation                                        |
| `style`   | formatting, missing semi colons, etc; no production code change     |
| `refactor`| refactoring production code, eg. renaming a variable                |
| `test`    | adding missing tests, refactoring tests; no production code change  |
| `chore`   | updating grunt tasks etc; no production code change                 |

Prepand `wip` (work in progress) if work isn't finished but should be pushed. Also, add a `Ref: <ticket-number>` in the description.

#### Example:
```
feat: parse definition in Spanish
ref: 1234
```