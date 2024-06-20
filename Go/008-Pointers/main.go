package main
import "fmt"

func main() {
   var name = "Max"
   var namePointer = &name
   fmt.Println(namePointer)
   fmt.Println(*namePointer)
}
