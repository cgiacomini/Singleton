package main
import "fmt"

func main() {

   greet()

   fmt.Println(greet2())

   fmt.Println(person())
   name, age := person()
   fmt.Println(name)
   fmt.Println(age)
}

func greet() {
   fmt.Println("hello!")
}


func greet2() string {
   return "Hello!!"
}


func person() (string, int) {
   return "Max", 23
}
