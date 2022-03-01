%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math import (assert_not_equal)
from starkware.cairo.common.alloc import alloc
from starkware.starknet.common.syscalls import get_caller_address

#########################

@storage_var
func registry_naive_idx_to_name (idx : felt) -> (name : felt):
end

@storage_var
func registry_naive_addr_to_idx (adr : felt) -> (idx : felt):
end

@storage_var
func registry_naive_size () -> (size : felt):
end


@view
func sns_lookup {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
        adr : felt
    ) -> (
        exist : felt,
        name : felt
    ):
    alloc_locals

    let (idx) = registry_naive_addr_to_idx.read (adr)

    local exist
    if idx == 0:
        exist = 0
    else:
        exist = 1
    end

    let (name) = registry_naive_idx_to_name.read (idx)

    return (exist, name)
end


@external
func sns_register {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
    name : felt) -> ():
    alloc_locals

    let (adr) = get_caller_address ()
    let (size) = registry_naive_size.read ()

    # O(n) sweep registery to find possible collision, revert if found
    _recurse_assert_not_found_in_registry (size, 0, name)

    # register; skipping index=0
    registry_naive_addr_to_idx.write (adr, size+1)
    registry_naive_idx_to_name.write (size+1, name)
    registry_naive_size.write (size + 1)

    return()
end

func _recurse_assert_not_found_in_registry {syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr} (
        len : felt,
        idx : felt,
        tgt : felt
    ) -> ():
    alloc_locals

    if idx == len:
        return ()
    end

    let (name) = registry_naive_idx_to_name.read (idx)
    assert_not_equal (name, tgt)

    _recurse_assert_not_found_in_registry (len, idx+1, tgt)
    return ()
end
