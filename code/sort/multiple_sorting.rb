
  def sort_tickets_by_comp_and_phone_verification!
    @tickets.sort! do |a, b|
      mobile_status_a = phone_status_to_i(a.member[:mobile_status])
      mobile_status_b = phone_status_to_i(b.member[:mobile_status])

      comp_comparison = a.comp.to_i <=> b.comp.to_i

      if comp_comparison != 0
        -(comp_comparison)
      elsif mobile_status_a == 3 && mobile_status_b == 3
        0
      elsif mobile_status_a == 3
        -1
      elsif mobile_status_b == 3
        1
      else
        compare_phone_status(b.member[:home_phone_status], a.member[:home_phone_status])
      end
    end

    # @tickets.sort! { |a, b| -(a.comp <=> b.comp) }
  end
