package main
import "fmt"

var name string
var age int
var adult bool
var height float32

var new_name string = "NewName"
var new_age, grade int = 15, 9

func main() {
  fmt.Println(name)
  fmt.Println(age)
  fmt.Println(adult)
  fmt.Println(height)

  name_2 := "Max"
  age_2 := 18

  fmt.Println(name_2)
  fmt.Println(age_2)

  var name_3 string = "Katerina"
  var age_3 int = 22

  fmt.Println(name_3)
  fmt.Println(age_3)

  var age_4 , grade_4 int = 1, 10

  fmt.Println(age_4)
  fmt.Println(grade_4)

  fmt.Println(new_age)
  fmt.Println(grade)

  //const name5 = "Max"
  //name5 = "toto"  <- this will not work
  //fmt.Println(name5)

}
