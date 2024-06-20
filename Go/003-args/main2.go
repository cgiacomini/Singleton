package main

import (
     "fmt" 
     "os"
)

func main() {
    arg0 :=os.Args[0]
    arg1 :=os.Args[1]
    fmt.Println(arg0)
    fmt.Println(arg1)
}
