# GO

```
$ go install github.com/onsi/ginkgo/ginkgo
$ go get github.com/onsi/ginkgo/v2
$ go get github.com/onsi/gomega

$ ginkgo version
Ginkgo Version 2.1.0
```

## Create Test dir
```
$ mkdir math-Ginkgo
$ cd math-Ginkgo
$ go mod init mathginkgo
$ ls
go.mod
```

## Create  functions file
Write several functions to be tested in the file maths/maths.go:
```
$ mkdir maths
$ cd maths
$ cat <<EOF > maths_functions.go
package maths_functions

// Add is our function that sums two integers
func Add(x, y int) (res int) {
    return x + y
}

// Subtract subtracts two integers
func Subtract(x, y int) (res int) {
    return x - y
}
EOF
```


## Generate a test template with the ginkgo command

```
$ cd maths
$ ginkgo bootstrap
Generating ginkgo test suite bootstrap for maths_functions in:
        maths_suite_test.go

$ ls
maths_functions.go  maths_suite_test.go
```
The ***maths_suite_test.go*** generated file has the following content
```
package maths_functions_test

import (
        "testing"

        . "github.com/onsi/ginkgo/v2"
        . "github.com/onsi/gomega"
)

func TestMaths(t *testing.T) {
        RegisterFailHandler(Fail)
        RunSpecs(t, "Maths Suite")
}

```

The newly generated ***target_funcs_suite_test.go*** does not have any test code yet
## Try to run the empty testsuite using ginkgo
```
$ ginkgo
Failed to compile maths:

# studyginkgo/maths
maths_suite_test.go:6:2: no required module provides package github.com/onsi/ginkgo; to add it:
        go get github.com/onsi/ginkgo
FAIL    studyginkgo/maths [setup failed]
FAIL

Ginkgo ran 1 suite in 921.2688ms
Test Suite Failed
```
**We need to add ginkgo module references**

```
go get github.com/onsi/ginkgo
$ go get github.com/onsi/ginkgo
go get: added github.com/fsnotify/fsnotify v1.4.9
go get: added github.com/nxadm/tail v1.4.8
go get: added github.com/onsi/ginkgo v1.16.5
go get: added golang.org/x/sys v0.0.0-20210112080510-489259a85091
go get: added gopkg.in/tomb.v1 v1.0.0-20141024135613-dd632973f1e7

```
**Try again**
```
$ ginkgo
Failed to compile maths:

# studyginkgo/maths
maths_suite_test.go:7:2: missing go.sum entry for module providing package github.com/onsi/gomega (imported by studyginkgo/maths); to add:
        go get -t studyginkgo/maths
FAIL    studyginkgo/maths [setup failed]
FAIL

Ginkgo ran 1 suite in 1.2583923s
Test Suite Failed
```

**We need to add our module **
```
$ go get -t studyginkgo/maths
go get -t studyginkgo/maths
```
**Try again - should work now**
```
$ ginkgo
Running Suite: Maths Suite
==========================
Random Seed: 1643110073
Will run 0 of 0 specs


Ran 0 of 0 Specs in 0.003 seconds
SUCCESS! -- 0 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

Ginkgo ran 1 suite in 5.8165437s
Test Suite Passed
```
## Try to run the empty testsuite using go
```
$ go test
Running Suite: Maths Suite
==========================
Random Seed: 1643110176
Will run 0 of 0 specs


Ran 0 of 0 Specs in 0.003 seconds
SUCCESS! -- 0 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS
ok      studyginkgo/maths       1.133s

```
## Try to run the empty testsuite using binary generated
ginkgo can compile the test code into a binary file
```
$ ginkgo build
Compiling maths...
    compiled maths.test

$ ls -lrt
total 8003
-rw-r--r-- 1 cgiacomini Domain Users     212 Jan 25 12:18 maths_functions.go
-rwxr-xr-x 1 cgiacomini Domain Users     198 Jan 25 12:19 maths_suite_test.go
-rwxr-xr-x 1 cgiacomini Domain Users 8192000 Jan 25 12:31 maths.test

$ ./maths.test
Running Suite: Maths Suite
==========================
Random Seed: 1643110319
Will run 0 of 0 specs


Ran 0 of 0 Specs in 0.003 seconds
SUCCESS! -- 0 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

```
## Write maths functions test code
Using ginkgo we can generate a test file
```
$ ginkgo generate maths_functions
Generating ginkgo test for MathsFunctions in:
  maths_functions_test.go
$ ls
maths.test  maths_functions.go  maths_functions_test.go  maths_suite_test.go
```
The above command generates the test maths_functions_test.go. If it is not in the $GOPATH directory, you may encounter the following error:
```
Couldn't identify package import path.

    ginkgo generate

Must be run within a package directory under $GOPATH/src/...
You're going to have to change UNKNOWN_PACKAGE_PATH in the generated file...
```
meaning that ginkgo probably does not support gomod yet. 
This error does not affect the usage, just modify UNKNOWN_PACKAGE_PATH in maths_functions_test.go to the package where it is located:
***maths_functions_test.go***
```
$ cat maths_functions_test.go
package maths_functions_test

import (
        . "github.com/onsi/ginkgo"
        . "github.com/onsi/gomega"

        "studyginkgo/maths"
)

var _ = Describe("MathsFunctions", func() {

})
```
Modify the file to fix the path for "studyginkgo/maths",
And also add our first test case as follow
***maths_functions_test.go***
```
$ cat maths_functions_test.go
package maths_functions_test

import (
        . "github.com/onsi/ginkgo"
        . "github.com/onsi/gomega"
        . "studyginkgo/maths"
)

var _ = Describe("MathsFunctions", func() {

        Describe("Add", func() {
            It("adds two numbers", func() {
                sum := Add(2,3)
                Expect(sum).To(Equal(5))
            })
       })
})
```
## Run the test case
```
$ ginkgo
Running Suite: Maths Suite
==========================
Random Seed: 1643118989
Will run 1 of 1 specs

+
Ran 1 of 1 Specs in 0.003 seconds
SUCCESS! -- 1 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

Ginkgo ran 1 suite in 3.9556717s
Test Suite Passed

```

Now, let’s say our requirements change and we’re only allowed to add positive numbers. 
Using the TDD process, let’s start by adding a failing test.
Modify ***maths_functions_test.go***  as follow: 

```
package maths_functions_test

import (
    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
    . "studyginkgo/maths"
)

var _ = Describe("MathsFunctions", func() {
    Describe("Add", func() {
        Context("when summands are positive", func() {
            It("adds two numbers", func() {
                sum, err := Add(2, 3)
                Expect(err).NotTo(HaveOccurred())
                Expect(sum).To(Equal(5))
            })
        })
        Context("when summand is negative", func() {
            It("returns an err", func() {
                _, err := Add(-1, -1)
                Expect(err).To(HaveOccurred())
            })
        })
    })
})

```

Run the test
```
$ ginkgo
Failed to compile maths:

# studyginkgo/maths_test [studyginkgo/maths.test]
.\maths_functions_test.go:13:14: assignment mismatch: 2 variables but maths_functions.Add returns 1 value
.\maths_functions_test.go:20:12: assignment mismatch: 2 variables but maths_functions.Add returns 1 value

Ginkgo ran 1 suite in 3.0525706s
Test Suite Failed
```
The **Add** function need to be changed accordingly to return errors in case of negative number sum
***maths_functions.go**

```
package maths_functions

import "errors"

var ErrInvalidSummand = errors.New("Invalid summand")


// Add is our function that sums two non negative integers
func Add(x, y int) (int, error) {
    if x <= 0 || y <= 0 {
        return 0, ErrInvalidSummand
    }
    return x + y, nil
}

// Subtract subtracts two integers
func Subtract(x, y int) (res int) {
    return x - y
}

```

Run the tests
```
$ ginkgo
Running Suite: Maths Suite
==========================
Random Seed: 1643119924
Will run 2 of 2 specs

++
Ran 2 of 2 Specs in 0.004 seconds
SUCCESS! -- 2 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

Ginkgo ran 1 suite in 4.5835209s
Test Suite Passe
```

## Add Suite function blocks

Ginkgo provide multiple types of functions blocks. In the above described file for example ***Describe*** is a function block.
In a testsuite file **maths_suite_test.go** we can encounter the following function blocs
* **BeforeSuite()** : Action to execute before the entire test starts
* **AfterSuite()** : Action to execute after the entire test is complete

```
package maths_functions_test

import (
    "testing"

    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
)

func TestMaths(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Maths Suite")
}

var _ = BeforeSuite(func() {
    println("BeforeSuite")
})

var _ = AfterSuite(func() {
    println("AfterSuite")
})

```
Run the tests
```
$ ginkgo
Running Suite: Maths Suite
==========================
Random Seed: 1643120437
Will run 2 of 2 specs

BeforeSuite
++AfterSuite

Ran 2 of 2 Specs in 0.004 seconds
SUCCESS! -- 2 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

Ginkgo ran 1 suite in 3.8631055s
Test Suite Passed

```

# Add test case functions blocs

In the test file **maths_functions_test** we can have the following functions blocks:
* **BeforeEach()** : The operation performed before each test case runs, located in Describe, there can be multiple
* **JustBeforeEach()** : Similar to BeforeEach(), executed after all BeforeEach() and before It()
* **AfterEach()** : Action to execute after each test case is run
* **JustAfterEach()** : executes immediately after It()
* **Describe()** : The top-level test case wrapping container, test cases of the same target, can be nested
* **Context()** : The test case wrapping container one level lower than Describe, the test case under the same condition
* **It()** : single test case, in Describe or Context
* **Specify()** : Alias ​​of It(), the purpose is exactly the same as It()
* **Measure()**: A block dedicated to performance testing, using the same scope as It():

## Modify maths_functions_test.go to adde the above functions call
***maths_functions_test.go***
```
package maths_functions_test

import (
    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
    . "studyginkgo/maths"
)

var _ = Describe("MathsFunctions", func() {
    Describe("Add", func() {
        Context("when summands are positive", func() {
            It("adds two numbers", func() {
                sum, err := Add(2, 3)
                Expect(err).NotTo(HaveOccurred())
                Expect(sum).To(Equal(5))
            })
        })
        Context("when summand is negative", func() {
            It("returns an err", func() {
                _, err := Add(-1, -1)
                Expect(err).To(HaveOccurred())
            })
        })

        BeforeEach(func() {
            println("BeforeEach-2")
        })

        BeforeEach(func() {
           println("BeforeEach-1")
        })

        JustBeforeEach(func() {
           println("JustBeforeEach-1")
        })

        JustBeforeEach(func() {
           println("JustBeforeEach-2")
        })

        JustAfterEach(func() {
           println("JustAfterEach-1")
        })

        JustAfterEach(func() {
           println("JustAfterEach-2")
        })

        AfterEach(func() {
           println("AfterEach-1")
        })

        AfterEach(func() {
          println("AfterEach-2")
        })
    })
})

```

Execute the tests case
```
$ ginkgo
Running Suite: Maths Suite
==========================
Random Seed: 1643121497
Will run 2 of 2 specs

BeforeSuite
BeforeEach-2
BeforeEach-1
JustBeforeEach-1
JustBeforeEach-2
JustAfterEach-1
JustAfterEach-2
AfterEach-1
AfterEach-2
+BeforeEach-2
BeforeEach-1
JustBeforeEach-1
JustBeforeEach-2
JustAfterEach-1
JustAfterEach-2
AfterEach-1
AfterEach-2
+AfterSuite

Ran 2 of 2 Specs in 0.004 seconds
SUCCESS! -- 2 Passed | 0 Failed | 0 Pending | 0 Skipped
PASS

Ginkgo ran 1 suite in 3.4896223s
Test Suite Passed
```


## Judgment of results
GinkGo provides multiple functions for numerical judgment
*Expect (actual interface{})* Create an assertion for the incoming parameter Assertion, Assertion supports the following judgment methods:
```
type Assertion interface { 
     Should(matcher types.GomegaMatcher, optionalDescription ...interface{}) 
	 boolShouldNot(matcher types.GomegaMatcher, optionalDescription ...interface{}) 
	 boolTo(matcher types.GomegaMatcher, optionalDescription ...interface{}) 
	 boolToNot(matcher types.GomegaMatcher, optionalDescription ...interface{}) 
	 boolNotTo(matcher types.GomegaMatcher, optionalDescription ...interface{}) bool
}
```
The first parameter of the assertion is matcher, defined in github.com/onsi/gomega/matcher.go, for example:
```
func BeNil() types.GomegaMatcher { return &matchers.BeNilMatcher{}} // BeTrue succeeds if actual is true
func BeTrue() types.GomegaMatcher { return &matchers.BeTrueMatcher{}}
```
Use examples to assign the values of Err and svc:
```
Expect(err).To(BeNil(), "unexpected error obtaining ingress-nginx service")Expect(svc). NotTo(BeNil(), "expected a service but none returned")
```

