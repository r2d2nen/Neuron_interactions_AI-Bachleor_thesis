! --- BEGIN AUTO-GENERATED ---
!   CMD: /net/home/borisc/cheft/master/make_chp_init_code NNLOsim_224.ini +potential_name=NNLOsim_224

! SUITABLE V3 parameters:
!   c_D:   -0.187318777021627D0
!   c_E:   -0.459795577229800D0

subroutine chp_preset_NNLOsim_224
    use idaho_chiral_potential

    implicit none

    call initialize_chiral_potential

    ! (proton, nucleon, neutron)
    call chp_set_mass_nucleon((/938.2720460000D0, 938.9182671179D0, 939.5653790000D0/))
    ! (pi-, pi, pi+)
    call chp_set_mass_pion((/139.5701800000D0, 134.9766000000D0, 139.5701800000D0/))

    call chp_set_chiral_order(NNLO)
    call chp_set_reg("SF", 700.000D0)
    call chp_set_itope("EM")
    call chp_set_contact_format("PW")

    call chp_set_gA(1.2900D0)
    call chp_set_fpi(92.4000D0)
    call chp_set_fine_structure(0.007297352569800D0)

    call chp_set_Lambda(500.000D0)

    call chp_set_c1(  -0.067540009009185D0)
    call chp_set_c3(  -3.581080069951500D0)
    call chp_set_c4(   3.519360609463700D0)

    call chp_set_CIB_LO_contact(1, -1,   -0.147958298068363D0) ! Ct_1S0pp
    call chp_set_CIB_LO_contact(2, -1,   -0.169402897810382D0) ! Ct_3S1pp
    call chp_set_CIB_LO_contact(1,  0,   -0.148749292556431D0) ! Ct_1S0np
    call chp_set_CIB_LO_contact(2,  0,   -0.169402897810382D0) ! Ct_3S1np
    call chp_set_CIB_LO_contact(1,  1,   -0.148575707454143D0) ! Ct_1S0nn
    call chp_set_CIB_LO_contact(2,  1,   -0.169402897810382D0) ! Ct_3S1nn

    call chp_set_NLO_contact(1,    2.501054251771210D0) ! C_1S0
    call chp_set_NLO_contact(2,    1.168314629591250D0) ! C_3P0
    call chp_set_NLO_contact(3,    0.446214871973325D0) ! C_1P1
    call chp_set_NLO_contact(4,   -0.923600681454642D0) ! C_3P1
    call chp_set_NLO_contact(5,    0.659950751270086D0) ! C_3S1
    call chp_set_NLO_contact(6,    0.543636932393351D0) ! C_3S1-3D1
    call chp_set_NLO_contact(7,   -0.662384473252353D0) ! C_3P2

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
    call chp_set_N3LO_contact_reg_par(1, 3.0D0) ! Dh_1S0
    call chp_set_N3LO_contact_reg_par(2, 3.0D0) ! D_1S0
    call chp_set_N3LO_contact_reg_par(3, 3.0D0) ! D_3P0
    call chp_set_N3LO_contact_reg_par(4, 3.0D0) ! D_1P1
    call chp_set_N3LO_contact_reg_par(5, 3.0D0) ! D_3P1
    call chp_set_N3LO_contact_reg_par(6, 3.0D0) ! Dh_3S1
    call chp_set_N3LO_contact_reg_par(7, 3.0D0) ! D_3S1
    call chp_set_N3LO_contact_reg_par(8, 3.0D0) ! D_3D1
    call chp_set_N3LO_contact_reg_par(9, 3.0D0) ! Dh_3S1-3D1
    call chp_set_N3LO_contact_reg_par(10, 3.0D0) ! D_3S1-3D1
    call chp_set_N3LO_contact_reg_par(11, 3.0D0) ! D_1D2
    call chp_set_N3LO_contact_reg_par(12, 3.0D0) ! D_3D2
    call chp_set_N3LO_contact_reg_par(13, 3.0D0) ! D_3P2
    call chp_set_N3LO_contact_reg_par(14, 3.0D0) ! D_3P2-3F2
    call chp_set_N3LO_contact_reg_par(15, 3.0D0) ! D_3D3

    call chp_set_2PE_CSB_correct_mass(0)

    call chp_set_2PE_2loop_int(1)

    call chp_set_2PE_1loop_r(0)

    call chp_set_units_and_derive_constants

end subroutine
! --- END AUTO-GENERATED ---
