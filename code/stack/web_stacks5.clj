(defn handler [req]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body "Hello World"})

(defn middleware [h & opt]
  (fn [req]
     (let [res (h req)]
        (transform res)))

(def app (-> handler middleware mw2 mw3))

(use 'ring.adapter.jetty)
(use 'hello-world.core)
(run-jetty app {:port 3000})
