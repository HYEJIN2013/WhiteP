 scope :done, -> { where( " status in ('DONE','FAIL') ").order('created_at DESC') }
  
  scope :running, lambda { |user| 
                        where( "status not in ('DONE', 'PENDING', 'FAIL')"  )
                       .where(:user_id => user.id)
                       .order('created_at DESC') 
                     }

  scope :pending, lambda { |user|
                            where( "status ='PENDING'"  )
                            .where(:user_id => user.id)
                            .order('created_at DESC') 
                         }
                         
  default_scope  do
    exclude_columns = %w(created_at updated_at dew_point_temperature visibility_distance precipitation_hour)
    filtered_cols = (column_names - exclude_columns.map(&:to_s)).map{|i| "weather_logs."+i}
    self.select(filtered_cols)
  end     
