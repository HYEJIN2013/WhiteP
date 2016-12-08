package org.testbed;

import java.util.*;
import java.util.function.*;
import java.util.stream.Collector;
import java.util.stream.Collectors;

/**
 * Created by kkim on 3/28/16.
 */
public class TestJavaFlatMap {

    /**
     * Created by kkim on 3/25/16.
     * [['a'], ['b', ['a']], ['c', ['b', ['a']]], ['d', ['c', ['b', ['a']]]], 'e']
     * ['a', 'b', 'a', 'c', 'b', 'a', 'd', 'c', 'b', 'a', 'e']
     *
     */

    public static List flat(List list) {
        List ret = new ArrayList();
        for (Object o : list)
            ret.addAll((o instanceof List)?flat((List)o):Arrays.asList(o));
        return ret;
    }


    public static void main(String[] args) {
        List<Integer> test1 = Arrays.asList(1,2,3);
        List<Integer> test2 = Arrays.asList(4,5);
        List<List<Integer>> test = new ArrayList<>();
        test.add(test1);
        test.add(test2);

        System.out.println(test.stream().flatMap(Collection::stream).collect(Collectors.toList()));
        System.out.println(flat(test));

        List a = Arrays.asList("a");
        List b = Arrays.asList("b",a);
        List c = Arrays.asList("c",b);
        List d = Arrays.asList("d",c);

        List data = Arrays.asList(a,b,c,d,"e");

        System.out.println(data);
        System.out.println(flat(data));

    }
}
