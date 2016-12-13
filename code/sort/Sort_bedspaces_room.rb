class Room < ActiveRecord::Base
  def to_s
    "#{building_floor.to_s}, #{Room.model_name.human} #{number}"
  end
end
