package com.sbk.callerid.service;

import com.sbk.callerid.model.CallerId;

import java.util.List;

public interface ICallerIdService
{
    void init();

    boolean add(CallerId record);

    List<CallerId> get(String number);

    boolean contains(String number);
}
