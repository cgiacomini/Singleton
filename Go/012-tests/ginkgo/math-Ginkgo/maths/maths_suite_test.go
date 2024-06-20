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

