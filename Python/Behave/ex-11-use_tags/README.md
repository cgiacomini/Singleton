TODO:	Add description with cucumber tag-expressions
Goal:	Understand the usage of tags to organize the testsuite and optimize test runs.
Several test frameworks support a concept of tags to mark a number of tests (py.test markers, TestNG test groups, JUnit Categories, NUnit CategoryAttribute). This provides a simple, flexible and effective mechanism to:

select a number of tests
exclude a number of tests
for a test run. This mechanism is orthogonal to the static test package structure.

Hint

Predefined or often used tags:

Tag	Kind	Description
@wip	predefined	“Work in Process” (under development).
@skip	predefined	Skip/disable a feature, scenario, …
@slow	user-defined	Mark slow, long-running tests.
Hint

Tag Logic:

Logic Operation	Command Options	Description
select/enable	--tags=@one	Only items with this tag.
not (tilde/minus)	--tags=~@one	Only items without this tag.
logical-or	--tags=@one,@two	If @one or @two is present.
logical-and	--tags=@one --tags=@two	If both @one and @two are present.
Notes:

The tag name prefix ‘@’ (AT) is optional in tag options
Use --tags-help for a short description of the tag logic.
See also behave tags documentation for more information on tags.


```
$ behave --tags=-wip
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 1 skipped
3 steps passed, 0 failed, 3 skipped, 0 undefined
Took 0m0.001s
```
**The whole feature is skipped**
```
$ behave --tags=ninja.chuck
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 1 skipped
3 steps passed, 0 failed, 3 skipped, 0 undefined
Took 0m0.001s
```
**only @ninja.chuck is executed**
```
$ behave --tags=-ninja.chuck
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 1 skipped
3 steps passed, 0 failed, 3 skipped, 0 undefined
Took 0m0.001s
```
**ninja.chuck is skipped**
```
$ behave --tags=@ninja.any,@ninja.chuck
1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
6 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.002s
```
**both scenarios are executed.**
```
$ behave --tags=@ninja.any --tags=@ninja.chuck
0 features passed, 0 failed, 1 skipped
0 scenarios passed, 0 failed, 2 skipped
0 steps passed, 0 failed, 6 skipped, 0 undefined
Took 0m0.000s
```
**Now no scenario is executed, all are skipped.**