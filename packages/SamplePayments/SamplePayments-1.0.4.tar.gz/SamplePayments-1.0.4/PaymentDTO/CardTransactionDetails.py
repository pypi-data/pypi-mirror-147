class CardTransactionDetails:

    @property
    def paymentTransactionId(self):
        return self.__paymentTransactionId

    @paymentTransactionId.setter
    def paymentTransactionId(self, var):
        self.__paymentTransactionId=var

    @property
    def merchantId(self):
        return self.__merchantId

    @merchantId.setter
    def merchantId(self, var):
        self.__merchantId=var

    @property
    def merchantOrderId(self):
        return self.__merchantOrderId

    @merchantOrderId.setter
    def merchantOrderId(self, var):
        self.__merchantOrderId=var

    @property
    def ipAddress(self):
        return self.__ipAddress

    @ipAddress.setter
    def ipAddress(self, var):
        self.__ipAddress=var

    @property
    def machineName(self):
        return self.__machineName

    @machineName.setter
    def machineName(self, var):
        self.__machineName=var

    @property
    def requestURL(self):
        return self.__requestURL

    @requestURL.setter
    def requestURL(self, var):
        self.__requestURL=var

    @property
    def createdDate(self):
        return self.__createdDate

    @createdDate.setter
    def createdDate(self, var):
        self.__createdDate=var

    @property
    def totalOrderAmount(self):
        return self.__totalOrderAmount

    @totalOrderAmount.setter
    def totalOrderAmount(self, var):
        self.__totalOrderAmount=var

    @property
    def cardNumberLast4Digit(self):
        return self.__cardNumberLast4Digit

    @cardNumberLast4Digit.setter
    def cardNumberLast4Digit(self, var):
        self.__cardNumberLast4Digit=var

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, var):
        self.__currency=var

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, var):
        self.__amount=var

    @property
    def paymentType(self):
        return self.__paymentType

    @paymentType.setter
    def paymentType(self, var):
        self.__paymentType=var

    @property
    def avsCode(self):
        return self.__avsCode

    @avsCode.setter
    def avsCode(self, var):
        self.__avsCode=var

    @property
    def avsCodeRaw(self):
        return self.__avsCodeRaw

    @avsCodeRaw.setter
    def avsCodeRaw(self, var):
        self.__avsCodeRaw=var

    @property
    def cardSubTypeId(self):
        return self.__cardSubTypeId

    @cardSubTypeId.setter
    def cardSubTypeId(self, var):
        self.__cardSubTypeId=var

    @property
    def cardTypeId(self):
        return self.__cardTypeId

    @cardTypeId.setter
    def cardTypeId(self, var):
        self.__cardTypeId=var

    @property
    def cardVerificationResultCode(self):
        return self.__cardVerificationResultCode

    @cardVerificationResultCode.setter
    def cardVerificationResultCode(self, var):
        self.__cardVerificationResultCode=var

    @property
    def cvvStatus(self):
        return self.__cvvStatus

    @cvvStatus.setter
    def cvvStatus(self, var):
        self.__cvvStatus=var

    @property
    def errorReason(self):
        return self.__errorReason

    @errorReason.setter
    def errorReason(self, var):
        self.__errorReason=var

    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, var):
        self.__errorMessage=var

    @property
    def errorField(self):
        return self.__errorField

    @errorField.setter
    def errorField(self, var):
        self.__errorField=var

    @property
    def errorFieldReason(self):
        return self.__errorFieldReason

    @errorFieldReason.setter
    def errorFieldReason(self, var):
        self.__errorFieldReason=var

    @property
    def httpResponseCode(self):
        return self.__httpResponseCode

    @httpResponseCode.setter
    def httpResponseCode(self, var):
        self.__httpResponseCode=var

    @property
    def httpResponseReason(self):
        return self.__httpResponseReason

    @httpResponseReason.setter
    def httpResponseReason(self, var):
        self.__httpResponseReason=var

    @property
    def processingStartTime(self):
        return self.__processingStartTime

    @processingStartTime.setter
    def processingStartTime(self, var):
        self.__processingStartTime=var

    @property
    def processingEndTime(self):
        return self.__processingEndTime

    @processingEndTime.setter
    def processingEndTime(self, var):
        self.__processingEndTime=var

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, var):
        self.__status=var
    
    @property
    def informationApprovalCode(self):
        return self.__informationApprovalCode

    @informationApprovalCode.setter
    def informationApprovalCode(self, var):
        self.__informationApprovalCode=var

    @property
    def informationResponseCode(self):
        return self.__informationResponseCode

    @informationResponseCode.setter
    def informationResponseCode(self, var):
        self.__informationResponseCode=var
        
    @property
    def orderSubmitTimeUtc(self):
        return self.__orderSubmitTimeUtc

    @orderSubmitTimeUtc.setter
    def orderSubmitTimeUtc(self, var):
        self.__orderSubmitTimeUtc=var
   
    @property
    def reconciliationId(self):
        return self.__reconciliationId

    @reconciliationId.setter
    def reconciliationId(self, var):
        self.__reconciliationId=var
        
    @property
    def processorRefundId(self):
        return self.__processorRefundId

    @processorRefundId.setter
    def processorRefundId(self, var):
        self.__processorRefundId=var

    @property
    def transactionId(self):
        return self.__transactionId

    @transactionId.setter
    def transactionId(self, var):
        self.__transactionId=var

    @property
    def capturePaymentResponseAmount(self):
        return self.__capturePaymentResponseAmount

    @capturePaymentResponseAmount.setter
    def capturePaymentResponseAmount(self, var):
        self.__capturePaymentResponseAmount=var

    @property
    def capturePaymentResponseCurrency(self):
        return self.__capturePaymentResponseCurrency

    @capturePaymentResponseCurrency.setter
    def capturePaymentResponseCurrency(self, var):
        self.__capturePaymentResponseCurrency=var

    @property
    def oldCardPaymentTransactionId(self):
        return self.__oldCardPaymentTransactionId

    @oldCardPaymentTransactionId.setter
    def oldCardPaymentTransactionId(self, var):
        self.__oldCardPaymentTransactionId=var

    @property
    def geoLocationId(self):
        return self.__geoLocationId

    @geoLocationId.setter
    def geoLocationId(self, var):
        self.__geoLocationId=var

    @property
    def paymentThru(self):
        return self.__paymentThru

    @paymentThru.setter
    def paymentThru(self, var):
        self.__paymentThru=var

    @property
    def paymentApp(self):
        return self.__paymentApp

    @paymentApp.setter
    def paymentApp(self, var):
        self.__paymentApp=var

    @property
    def paymentAppType(self):
        return self.__paymentAppType

    @paymentAppType.setter
    def paymentAppType(self, var):
        self.__paymentAppType=var

    @property
    def modeOfPayment(self):
        return self.__modeOfPayment

    @modeOfPayment.setter
    def modeOfPayment(self, var):
        self.__modeOfPayment=var