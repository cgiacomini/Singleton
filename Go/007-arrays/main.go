package main
import "fmt"

func main() {
   var students = [2] string {"Max","Anna"}
   fmt.Println(students)

   var students2 [2] string
   students2[0] = "Pino"
   students2[1] = "Lucio"
   fmt.Println(students2)

   var students3 [] string
   students3 = append(students3, "Freddy")
   students3 = append(students3, "Edo")
   students3 = append(students3, "Sandy")
   students3 = append(students3, "Romeo")
   fmt.Println(students3)

   for i, value := range students3 {
      fmt.Println(i,value)
   }


   for _, value := range students3 {
      fmt.Println(value)
   }
}
