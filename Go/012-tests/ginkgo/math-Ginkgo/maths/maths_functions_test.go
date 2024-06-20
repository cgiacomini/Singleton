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
