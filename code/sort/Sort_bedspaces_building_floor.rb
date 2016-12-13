class BuildingFloor < ActiveRecord::Base
  def to_s
    "#{building.to_s}, #{self.class.model_name.human} #{number}"
  end
end
