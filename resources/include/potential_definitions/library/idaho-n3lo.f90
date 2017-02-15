! --- BEGIN AUTO-GENERATED ---
!   CMD: ./../make_chp_init_code ns-input.ini +potential_name=idaho_n3lo

subroutine chp_preset_idaho_n3lo
    use idaho_chiral_potential

    implicit none

    call initialize_chiral_potential

    ! (proton, nucleon, neutron)
    call chp_set_mass_nucleon((/938.2720000000D0, 938.9182046406D0, 939.5653000000D0/))
    ! (pi-, pi, pi+)
    call chp_set_mass_pion((/139.5702000000D0, 134.9766000000D0, 139.5702000000D0/))

    call chp_set_chiral_order(N3LO)
    call chp_set_reg("DR", 0.000D0)
    call chp_set_itope("EM")
    call chp_set_contact_format("PW")

    call chp_set_gA(1.2900D0)
    call chp_set_fpi(92.4000D0)
    call chp_set_fine_structure(0.007296795700718D0)

    call chp_set_Lambda(500.000D0)

    call chp_set_c1(  -0.810000000000000D0)
    call chp_set_c3(  -3.200000000000000D0)
    call chp_set_c4(   5.400000000000000D0)
    call chp_set_c2           (   2.800000000000000D0)
    call chp_set_d1_plus_d2   (   3.060000000000000D0)
    call chp_set_d3           (  -3.270000000000000D0)
    call chp_set_d5           (   0.450000000000000D0)
    call chp_set_d14_minus_d15(  -5.650000000000000D0)

    call chp_set_CIB_LO_contact(1, -1,   -0.145286000000000D0) ! Ct_1S0pp
    call chp_set_CIB_LO_contact(2, -1,   -0.118972496000000D0) ! Ct_3S1pp
    call chp_set_CIB_LO_contact(1,  0,   -0.147167000000000D0) ! Ct_1S0np
    call chp_set_CIB_LO_contact(2,  0,   -0.118972496000000D0) ! Ct_3S1np
    call chp_set_CIB_LO_contact(1,  1,   -0.146285000000000D0) ! Ct_1S0nn
    call chp_set_CIB_LO_contact(2,  1,   -0.118972496000000D0) ! Ct_3S1nn

    call chp_set_NLO_contact(1,    2.380000000000000D0) ! C_1S0
    call chp_set_NLO_contact(2,    1.487000000000000D0) ! C_3P0
    call chp_set_NLO_contact(3,    0.656000000000000D0) ! C_1P1
    call chp_set_NLO_contact(4,   -0.630000000000000D0) ! C_3P1
    call chp_set_NLO_contact(5,    0.760000000000000D0) ! C_3S1
    call chp_set_NLO_contact(6,    0.826000000000000D0) ! C_3S1-3D1
    call chp_set_NLO_contact(7,   -0.538000000000000D0) ! C_3P2

    call chp_set_N3LO_contact( 1,   -2.545000000000000D0) ! Dh_1S0
    call chp_set_N3LO_contact( 2,  -16.000000000000000D0) ! D_1S0
    call chp_set_N3LO_contact( 3,    0.245000000000000D0) ! D_3P0
    call chp_set_N3LO_contact( 4,    5.250000000000000D0) ! D_1P1
    call chp_set_N3LO_contact( 5,    2.350000000000000D0) ! D_3P1
    call chp_set_N3LO_contact( 6,    7.000000000000001D0) ! Dh_3S1
    call chp_set_N3LO_contact( 7,    6.550000000000000D0) ! D_3S1
    call chp_set_N3LO_contact( 8,   -2.800000000000000D0) ! D_3D1
    call chp_set_N3LO_contact( 9,    2.250000000000000D0) ! Dh_3S1-3D1
    call chp_set_N3LO_contact(10,    6.610000000000000D0) ! D_3S1-3D1
    call chp_set_N3LO_contact(11,   -1.770000000000000D0) ! D_1D2
    call chp_set_N3LO_contact(12,   -1.460000000000000D0) ! D_3D2
    call chp_set_N3LO_contact(13,    2.295000000000000D0) ! D_3P2
    call chp_set_N3LO_contact(14,   -0.465000000000000D0) ! D_3P2-3F2
    call chp_set_N3LO_contact(15,    5.660000000000000D0) ! D_3D3

    call chp_set_1PE_reg_par(4.0D0)
    call chp_set_2PE_reg_par(2.0D0)
    call chp_set_LO_contact_reg_par(1, 3.0D0) ! Ct_1S0
    call chp_set_LO_contact_reg_par(2, 3.0D0) ! Ct_3S1
    call chp_set_NLO_contact_reg_par(1, 2.0D0) ! C_1S0
    call chp_set_NLO_contact_reg_par(2, 2.0D0) ! C_3P0
    call chp_set_NLO_contact_reg_par(3, 2.0D0) ! C_1P1
    call chp_set_NLO_contact_reg_par(4, 2.0D0) ! C_3P1
    call chp_set_NLO_contact_reg_par(5, 2.0D0) ! C_3S1
    call chp_set_NLO_contact_reg_par(6, 2.0D0) ! C_3S1-3D1
    call chp_set_NLO_contact_reg_par(7, 2.0D0) ! C_3P2
    call chp_set_N3LO_contact_reg_par(1, 2.0D0) ! Dh_1S0
    call chp_set_N3LO_contact_reg_par(2, 2.0D0) ! D_1S0
    call chp_set_N3LO_contact_reg_par(3, 3.0D0) ! D_3P0
    call chp_set_N3LO_contact_reg_par(4, 2.0D0) ! D_1P1
    call chp_set_N3LO_contact_reg_par(5, 4.0D0) ! D_3P1
    call chp_set_N3LO_contact_reg_par(6, 2.0D0) ! Dh_3S1
    call chp_set_N3LO_contact_reg_par(7, 2.0D0) ! D_3S1
    call chp_set_N3LO_contact_reg_par(8, 2.0D0) ! D_3D1
    call chp_set_N3LO_contact_reg_par(9, 2.0D0) ! Dh_3S1-3D1
    call chp_set_N3LO_contact_reg_par(10, 2.0D0) ! D_3S1-3D1
    call chp_set_N3LO_contact_reg_par(11, 4.0D0) ! D_1D2
    call chp_set_N3LO_contact_reg_par(12, 2.0D0) ! D_3D2
    call chp_set_N3LO_contact_reg_par(13, 2.0D0) ! D_3P2
    call chp_set_N3LO_contact_reg_par(14, 4.0D0) ! D_3P2-3F2
    call chp_set_N3LO_contact_reg_par(15, -1.0D0) ! D_3D3

    call chp_set_2PE_CSB_correct_mass(1)

    call chp_set_2PE_2loop_int(0)

    call chp_set_units_and_derive_constants

end subroutine
! --- END AUTO-GENERATED ---
