package org.testbed

/**
  * Created by kkim on 3/28/16.
  */
object TestFlatMap {

  def flatMap(in : List[Any] ): List[Any] =
    in.foldLeft(List[Any]())((result,elem) =>
      elem match  {
        case _: List[Any] => result ++ flatMap(elem.asInstanceOf[List[Any]])
        case _ => result :+ elem
      }
    )


  def main(args: Array[String]) {
    val lista = List[Any]("a")
    val listb = List[Any]("b",lista)
    val listc = List[Any]("c",listb)
    val listd = List[Any]("d",listc)
    val data = List[Any](lista,listb,listc,listd,"e")

    println(flatMap(data))

  }

}
