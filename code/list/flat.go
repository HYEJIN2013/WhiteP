package main

import (
        "fmt"

)

func flat(list []interface{}) []interface{} {
	var ret []interface{}

	for _,v := range list {
		switch t := v.(type) {
		default:
			ret = append(ret,t)
		case []interface{}:
			for _, e :=range flat(t) {
				ret = append(ret,e)
			}
		}

	}
	return ret
}

func main()  {

        lista := []interface{} {"a"}
	listb := []interface{} {"b",lista}
	listc := []interface{} {"c",listb}
	listd := []interface{} {"d",listc}
        data := []interface{} { lista, listb, listc, listd, "e"}

	fmt.Println(data)
	fmt.Println(flat(data))

}
