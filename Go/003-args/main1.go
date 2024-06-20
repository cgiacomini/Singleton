package main
import "fmt"

func main() {
   fmt.Println("Enter something: ")
   var first string
   fmt.Scanln(&first)
   fmt.Print("Input: " + first + "\n")
   fmt.Println("Input: " + first + "\n")
}
