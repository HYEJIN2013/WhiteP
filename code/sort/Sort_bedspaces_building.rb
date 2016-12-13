class Building < ActiveRecord::Base
  def to_s
    "#{self.class.model_name.human} #{number}"
  end
end
