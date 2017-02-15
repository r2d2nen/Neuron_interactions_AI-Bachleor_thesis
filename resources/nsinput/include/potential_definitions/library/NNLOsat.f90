! --- BEGIN AUTO-GENERATED ---
!   CMD: ./../make_chp_init_code ns-input.ini +potential_name=nnlo_sat

! SUITABLE V3 parameters:
!   c_D:    0.816805891482710D0
!   c_E:   -0.039574712703510D0

subroutine chp_preset_nnlo_sat
    use idaho_chiral_potential

    implicit none

    call initialize_chiral_potential

    ! (proton, nucleon, neutron)
    call chp_set_mass_nucleon((/938.2720000000D0, 938.9184000000D0, 939.5653000000D0/))
    ! (pi-, pi, pi+)
    call chp_set_mass_pion((/139.5702000000D0, 134.9766000000D0, 139.5702000000D0/))

    call chp_set_chiral_order(NNLO)
    call chp_set_reg("SF", 700.000D0)
    call chp_set_itope("EM")
    call chp_set_contact_format("PW")

    call chp_set_gA(1.2900D0)
    call chp_set_fpi(92.4000D0)
    call chp_set_fine_structure(0.007297352570000D0)

    call chp_set_Lambda(450.000D0)

    call chp_set_c1(  -1.121521199632590D0)
    call chp_set_c3(  -3.925005856486820D0)
    call chp_set_c4(   3.765687158585920D0)

    call chp_set_CIB_LO_contact(1, -1,   -0.158149379370110D0) ! Ct_1S0pp
    call chp_set_CIB_LO_contact(2, -1,   -0.177674364499000D0) ! Ct_3S1pp
    call chp_set_CIB_LO_contact(1,  0,   -0.159822449578320D0) ! Ct_1S0np
    call chp_set_CIB_LO_contact(2,  0,   -0.177674364499000D0) ! Ct_3S1np
    call chp_set_CIB_LO_contact(1,  1,   -0.159150268280180D0) ! Ct_1S0nn
    call chp_set_CIB_LO_contact(2,  1,   -0.177674364499000D0) ! Ct_3S1nn

    call chp_set_NLO_contact(1,    2.539367785050380D0) ! C_1S0
    call chp_set_NLO_contact(2,    1.398365591876140D0) ! C_3P0
    call chp_set_NLO_contact(3,    0.555958765133350D0) ! C_1P1
    call chp_set_NLO_contact(4,   -1.136095263327820D0) ! C_3P1
    call chp_set_NLO_contact(5,    1.002892673483510D0) ! C_3S1
    call chp_set_NLO_contact(6,    0.600716048335960D0) ! C_3S1-3D1
    call chp_set_NLO_contact(7,   -0.802300295338460D0) ! C_3P2

    call chp_set_1PE_reg_par(3.0D0)
    call chp_set_2PE_reg_par(3.0D0)
    call chp_set_LO_contact_reg_par(1, 3.0D0) ! Ct_1S0
    call chp_set_LO_contact_reg_par(2, 3.0D0) ! Ct_3S1
    call chp_set_NLO_contact_reg_par(1, 3.0D0) ! C_1S0
    call chp_set_NLO_contact_reg_par(2, 3.0D0) ! C_3P0
    call chp_set_NLO_contact_reg_par(3, 3.0D0) ! C_1P1
    call chp_set_NLO_contact_reg_par(4, 3.0D0) ! C_3P1
    call chp_set_NLO_contact_reg_par(5, 3.0D0) ! C_3S1
    call chp_set_NLO_contact_reg_par(6, 3.0D0) ! C_3S1-3D1
    call chp_set_NLO_contact_reg_par(7, 3.0D0) ! C_3P2

    call chp_set_2PE_CSB_correct_mass(0)

    call chp_set_2PE_2loop_int(1)

    call chp_set_units_and_derive_constants

end subroutine
! --- END AUTO-GENERATED ---
