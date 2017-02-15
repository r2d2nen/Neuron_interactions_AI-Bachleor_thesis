! --- BEGIN AUTO-GENERATED ---
!   CMD: ./../make_chp_init_code ns-input.ini +potential_name=nnlo_opt

subroutine chp_preset_nnlo_opt
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

    call chp_set_Lambda(500.000D0)

    call chp_set_c1(  -0.918639528734720D0)
    call chp_set_c3(  -3.888687492763241D0)
    call chp_set_c4(   4.310327160829740D0)

    call chp_set_CIB_LO_contact(1, -1,   -0.151366037203108D0) ! Ct_1S0pp
    call chp_set_CIB_LO_contact(2, -1,   -0.158434176622812D0) ! Ct_3S1pp
    call chp_set_CIB_LO_contact(1,  0,   -0.152141088236679D0) ! Ct_1S0np
    call chp_set_CIB_LO_contact(2,  0,   -0.158434176622812D0) ! Ct_3S1np
    call chp_set_CIB_LO_contact(1,  1,   -0.151764745900691D0) ! Ct_1S0nn
    call chp_set_CIB_LO_contact(2,  1,   -0.158434176622812D0) ! Ct_3S1nn

    call chp_set_NLO_contact(1,    2.404021944134705D0) ! C_1S0
    call chp_set_NLO_contact(2,    1.263390763475578D0) ! C_3P0
    call chp_set_NLO_contact(3,    0.417045542055649D0) ! C_1P1
    call chp_set_NLO_contact(4,   -0.782658499975205D0) ! C_3P1
    call chp_set_NLO_contact(5,    0.928384662662304D0) ! C_3S1
    call chp_set_NLO_contact(6,    0.618141419047458D0) ! C_3S1-3D1
    call chp_set_NLO_contact(7,   -0.677808511406356D0) ! C_3P2

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

    call chp_set_2PE_CSB_correct_mass(1)

    call chp_set_2PE_2loop_int(1)

    call chp_set_units_and_derive_constants

end subroutine
! --- END AUTO-GENERATED ---
