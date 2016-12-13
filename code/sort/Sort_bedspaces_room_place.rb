class RoomPlace < ActiveRecord::Base
  def to_s
    "#{room.to_s}, #{I18n.t("room_place_number")} #{number}"
  end
  alias :name :to_s
end
