%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math import (assert_not_equal, assert_not_zero)
from starkware.cairo.common.alloc import alloc
from starkware.starknet.common.syscalls import get_caller_address


@storage_var
func registry_adr_to_name (idx : felt) -> (name : felt):
end

@storage_var
func registry_name_to_adr (adr : felt) -> (idx : felt):
end


@view
func sns_lookup_adr_to_name {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
        adr : felt
    ) -> (
        exist : felt,
        name : felt
    ):
    alloc_locals

    let (name) = registry_adr_to_name.read (adr)

    local exist
    if name == 0:
        assert exist = 0
    else:
        assert exist = 1
    end

    return (exist, name)
end

@view
func sns_lookup_name_to_adr {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
        name : felt
    ) -> (
        exist : felt,
        adr : felt
    ):
    alloc_locals

    let (adr) = registry_name_to_adr.read (name)

    local exist
    if adr == 0:
        assert exist = 0
    else:
        assert exist = 1
    end

    return (exist, adr)
end


#
# register adr -> name mapping in registry
# can only call from the address itself i.e. no delegate call allowed
#
@external
func sns_register {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
    name : felt) -> ():
    alloc_locals

    # TODO: check if name is a string literal i.e. valid ascii encoding

    let (adr) = get_caller_address ()

    #
    # Revert if the given name has already been registered with an address in the registry
    # (zero address is not valid)
    # this function reverts also if caller address tries to re-register with the same name
    #
    let (adr_check) = registry_name_to_adr.read (name)
    assert adr_check = 0

    # Register adr <=> name
    registry_adr_to_name.write (adr, name)
    registry_name_to_adr.write (name, adr)

    return()
end
