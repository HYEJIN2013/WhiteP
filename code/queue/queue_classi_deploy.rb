  namespace :qc do
    desc "start queue classic"
    task :start do
      run "nohup sh #{current_path}/qc_worker start > /dev/null 2>&1 &"
    end

    desc "stop queue classic"
    task :stop do
      run "sh #{current_path}/qc_worker stop"
    end
  end
