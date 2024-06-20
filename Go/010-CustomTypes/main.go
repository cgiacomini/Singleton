package main
import "fmt"

type student struct {
  name string 
  rate int
}


func main() {
   var students [] student
   students = append(students, student{"Maria", 15})
   students = append(students, student{"Sergio", 19})
   for _, s := range students {
      fmt.Println(s)
   }
}
