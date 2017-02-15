! --- BEGIN AUTO-GENERATED ---
!   CMD: ./make_chp_init_code NLOsim-450-158.ini +potential_name=NLOsim_158

subroutine chp_preset_NLOsim_158
    use idaho_chiral_potential

    implicit none

    call initialize_chiral_potential

    ! (proton, nucleon, neutron)
    call chp_set_mass_nucleon((/938.2720460000D0, 938.9182671179D0, 939.5653790000D0/))
    ! (pi-, pi, pi+)
    call chp_set_mass_pion((/139.5701800000D0, 134.9766000000D0, 139.5701800000D0/))

    call chp_set_chiral_order(NLO)
    call chp_set_reg("SF", 700.000D0)
    call chp_set_itope("EM")
    call chp_set_contact_format("PW")

    call chp_set_gA(1.2900D0)
    call chp_set_fpi(92.4000D0)
    call chp_set_fine_structure(0.007297352569800D0)

    call chp_set_Lambda(450.000D0)

    call chp_set_CIB_LO_contact(1, -1,   -0.155082508252056D0) ! Ct_1S0pp
    call chp_set_CIB_LO_contact(2, -1,   -0.184645985961860D0) ! Ct_3S1pp
    call chp_set_CIB_LO_contact(1,  0,   -0.156405979842647D0) ! Ct_1S0np
    call chp_set_CIB_LO_contact(2,  0,   -0.184645985961860D0) ! Ct_3S1np
    call chp_set_CIB_LO_contact(1,  1,   -0.155869880698231D0) ! Ct_1S0nn
    call chp_set_CIB_LO_contact(2,  1,   -0.184645985961860D0) ! Ct_3S1nn

    call chp_set_NLO_contact(1,    1.647993491368130D0) ! C_1S0
    call chp_set_NLO_contact(2,    1.269352678128980D0) ! C_3P0
    call chp_set_NLO_contact(3,    1.085888231722920D0) ! C_1P1
    call chp_set_NLO_contact(4,   -0.369069763865571D0) ! C_3P1
    call chp_set_NLO_contact(5,   -0.264805599252195D0) ! C_3S1
    call chp_set_NLO_contact(6,    0.182747621164870D0) ! C_3S1-3D1
    call chp_set_NLO_contact(7,   -0.249373759305687D0) ! C_3P2

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

    call chp_set_2PE_1loop_r(1)

    call chp_set_units_and_derive_constants

end subroutine
! --- END AUTO-GENERATED ---
